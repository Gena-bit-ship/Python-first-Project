from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton
)

# --- 1. REPLY-КЛАВИАТУРА (Нижнее главное меню) ---
def get_main_menu() -> ReplyKeyboardMarkup:
    kb = [
        [
            KeyboardButton(text="🔥 Свежие новости"),
            KeyboardButton(text="ℹ️ О боте")
        ],
        [
            KeyboardButton(text="⚙️ Стек технологий")
        ]
    ]
    return ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выбери действие из меню..."
    )

def get_article_inline_kb(article_url: str) -> InlineKeyboardMarkup:
    inline_kb = [
        [
            InlineKeyboardButton(text="Читать на Хабре 🔗", url=article_url)
        ],
        [
            InlineKeyboardButton(text="👍 Полезно", callback_data="like_news"),
            InlineKeyboardButton(text="👎 Не интересно", callback_data="dislike_news")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb)
