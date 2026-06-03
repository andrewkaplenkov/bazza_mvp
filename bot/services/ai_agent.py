from groq import Groq
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict
from config import GROQ_API_KEY, GROQ_MODEL, SYSTEM_PROMPT
import asyncio


class AIAgent:

    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)
        self.executor = ThreadPoolExecutor(max_workers=1)
        self.model = GROQ_MODEL
        self.system_prompt = SYSTEM_PROMPT

    async def generate_answer(self, question: str, context: List[Dict]) -> str:

        context_text = self._format_context(context)

        user_prompt = f"""Контекст из базы знаний:
{context_text}

Вопрос клиента: {question}

Сформулируй понятный и полезный ответ на основе предоставленной информации."""

        try:
            loop = asyncio.get_event_loop()

            completion = await loop.run_in_executor(
                self.executor,
                lambda: self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": self.system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.7,
                    max_tokens=1000,
                    top_p=1,
                )
            )

            answer = completion.choices[0].message.content
            return answer.strip()

        except Exception as e:
            print(f"Ошибка Groq API: {e}")
            return self._fallback_answer(context)

    def _format_context(self, context: List[Dict]) -> str:
        if not context:
            return "Информация не найдена в базе знаний."

        formatted = []
        for i, item in enumerate(context, 1):
            question = item.get("question", "")
            answer = item.get("answer", "")
            category = item.get("category", "")

            formatted.append(f"{i}. Вопрос: {question}")
            if category:
                formatted.append(f"   Категория: {category}")
            formatted.append(f"   Ответ: {answer}")
            formatted.append("")

        return "\n".join(formatted)

    def _fallback_answer(self, context: List[Dict]) -> str:
        if context:
            best = context[0]
            return f"📋 {best.get('answer', 'Извините, не могу ответить на этот вопрос.')}"

        return (
            "Извините, я не смог найти ответ на ваш вопрос.\n\n"
            "Вы можете связаться с нашим менеджером:\n"
            "Екатеринбург: Яна Крылосова, +79001974433, @yanakrylosovaa\n"
            "Москва: Алёна Дружинина, +79028096955, @druzhinina_alena"
        )