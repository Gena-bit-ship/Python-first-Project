import logging
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiohttp import ClientSession
from bs4 import BeautifulSoup

from app.keyboards import get_main_menu, get_article_inline_kb


router = Router()

async def parse_habr_news() -> list[dict]:
    """Асинхронный парсинг последних новостей с Хабра"""
    url = "https://habr.com/ru/news/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    async with ClientSession() as session:
        try:
            async with session.get(url, headers=headers, timeout=10) as response:
                if response.status != 200:
                    return []
                html = await response.text()
                soup = BeautifulSoup(html, "lxml")
                articles = []
                snippets = soup.find_all("a", class_="tm-title__link", limit=3)
                for snippet in snippets:
                    title = snippet.get_text(strip=True)
                    link = "https://habr.com" + snippet.get("href")
                    articles.append({"title": title, "link": link})
                return articles
        except Exception as e:
            logging.error(f"Ошибка при парсинге: {e}")
            return []

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "👋 **Здорово! Я асинхронный бот-парсер.**\n\n"
        "Используй меню снизу, чтобы управлять ботом!",
        reply_markup=get_main_menu(),
        parse_mode=ParseMode.MARKDOWN
    )

@router.message(F.text == "🔥 Свежие новости")
async def process_news_btn(message: types.Message):
    await message.answer("🔄 Выполняю асинхронный HTTP-запрос к Хабру...")
    news = await parse_habr_news()
    if not news:
        await message.answer("❌ Не удалось получить данные.")
        return
    
    for item in news:
        await message.answer(
            f"📰 **{item['title']}**",
            reply_markup=get_article_inline_kb(item['link']), # Добавляем кнопки под новость
            parse_mode=ParseMode.MARKDOWN
        )

@router.message(F.text == "ℹ️ О боте")
async def process_about_btn(message: types.Message):
    await message.answer(
        "🤖 **Инфа о боте:**\n\n"
        "• Разработчик: Геннадий\n"
        "• Архитектура: `aiogram 3` (Routers + Keyboards)\n"
        "• Работает асинхронно 24/7 на VPS сервере!",
        parse_mode=ParseMode.MARKDOWN
    )

@router.callback_query(F.data.in_({"like_news", "dislike_news"}))
async def process_feedback(callback: types.CallbackQuery):
    if callback.data == "like_news":
        await callback.answer("Спасибо за фидбек! 👍", show_alert=False)
    else:
        await callback.answer("Принято, будем улучшать подборку! 👎", show_alert=False)