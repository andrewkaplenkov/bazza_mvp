import aiohttp
import os
from typing import List, Dict, Optional

API_URL = os.getenv("API_URL", "http://backend:8000")


class BackendClient:

    def __init__(self):
        self.base_url = API_URL.rstrip("/")

    async def search_knowledge(self, query: str) -> List[Dict]:
        url = f"{self.base_url}/knowledge/"

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        all_kb = await response.json()
                        return self._filter_relevant(query.lower(), all_kb)
                    return []
        except Exception as e:
            print(f"Ошибка запроса к бэкенду: {e}")
            return []

    def _filter_relevant(self, query: str, all_kb: List[Dict], top_n: int = 3) -> List[Dict]:

        scored = []
        query_words = set(query.split())

        for item in all_kb:
            score = 0
            question_words = set(item.get("question", "").lower().split())
            score += len(query_words & question_words) * 2

            if item.get("category") and item["category"].lower() in query_words:
                score += 3

            answer_words = set(item.get("answer", "").lower().split())
            score += len(query_words & answer_words)

            if score > 0:
                scored.append((score, item))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [item for _, item in scored[:top_n]]

    async def get_projects(self) -> List[Dict]:
        url = f"{self.base_url}/projects/"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        return await response.json()
                    return []
        except Exception as e:
            print(f"Ошибка получения проектов: {e}")
            return []