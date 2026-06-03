from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from services.backend import BackendClient
from services.ai_agent import AIAgent

router = Router()

backend = BackendClient()
ai_agent = AIAgent()


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Привет! Я — умный помощник BAZA Development. \n\n"
        "Я знаю всё о наших жилых комплексах, ипотеке и условиях для партнеров.\n\n"
        "Просто напишите мне свой вопрос, например:\n"
        "— Какие ЖК сейчас в продаже?\n"
        "— Какая отделка в ЖК Алиса?\n"
        "— Какое агентское вознаграждение?"
    )


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "*Доступные команды:*\n\n"
        "/start - Запустить бота и узнать, что он умеет\n"
        "/projects - Посмотреть список всех ЖК\n"
        "/help - Показать эту справку\n\n"
        "*Совет:* Вы можете не использовать команды, а просто писать свои вопросы в чат в свободной форме!",
        parse_mode="Markdown"
    )


@router.message(Command("projects"))
async def cmd_projects(message: Message):
    await message.answer("Ищу актуальные проекты...")

    projects = await backend.get_projects()

    if not projects:
        await message.answer("Сейчас нет активных проектов в базе.")
        return

    text = "*Актуальные проекты BAZA:*\n\n"
    for p in projects:
        text += f"*{p['name']}*\n"
        text += f"   Город: {p['city']}\n"
        if p.get('completion_date'):
            text += f"   Сдача: {p['completion_date']}\n"
        text += "\n"

    await message.answer(text, parse_mode="Markdown")