import pytest
from unittest.mock import MagicMock
from src.bot import TelegramBot
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext


@pytest.fixture
def mock_bot():
    """مورد آزمایشی ربات با شبیه‌سازی پیام‌ها و پاسخ‌ها"""
    bot = TelegramBot(token="dummy_token")
    bot.application = MagicMock()  # شبیه‌سازی متدهای application
    return bot


@pytest.mark.asyncio
async def test_start(mock_bot):
    """تست برای بررسی درست بودن پیامی که در start ارسال می‌شود"""
    update = MagicMock(spec=Update)
    update.message.reply_text = MagicMock()

    await mock_bot.start(update, MagicMock())

    update.message.reply_text.assert_called_once_with(
        "سلام! 👋\nبه ربات خوش آمدید! لطفا یک گزینه را انتخاب کنید:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📖 نمایش محتوا", callback_data="show_content")],
            [InlineKeyboardButton("🔍 جستجو", callback_data="search")],
            [InlineKeyboardButton("❤️ علاقه‌مندی‌ها", callback_data="show_favorites")]
        ])
    )
