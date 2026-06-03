from aiogram import Router, F
from aiogram.types import Message

from services.backend import BackendClient
from services.ai_agent import AIAgent

router = Router()

backend = BackendClient()
ai_agent = AIAgent()


@router.message(F.text)
async def handle_message(message: Message):

    user_question = message.text.strip()

    thinking_msg = await message.answer("Думаю...")

    try:
        context = await backend.search_knowledge(user_question)

        if not context:
            await thinking_msg.edit_text(
                "Извините, я не нашел информацию по вашему вопросу.\n\n"
                "Попробуйте переформулировать или свяжитесь с менеджером:\n"
                "Екатеринбург: Яна Крылосова, +79001974433, @yanakrylosovaa\n"
                "Москва: Алёна Дружинина, +79028096955, @druzhinina_alena"
            )
            return

        answer = await ai_agent.generate_answer(user_question, context)

        await thinking_msg.edit_text(answer)

    except Exception as e:
        print(f"Ошибка обработки сообщения: {e}")
        await thinking_msg.edit_text(
            "Произошла ошибка при обработке вашего вопроса. Попробуйте позже или свяжитесь с менеджером."
        )