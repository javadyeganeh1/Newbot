import pytest
from unittest.mock import MagicMock
from telegram import Update
from bot import TelegramBot

@pytest.fixture
def bot():
    bot = TelegramBot("dummy_token")
    bot.application = MagicMock()  # Mock the Telegram Application
    return bot

def test_start(bot):
    # Simulate the start command
    update = MagicMock(spec=Update)
    update.message.reply_text = MagicMock()
    bot.start(update, None)
    update.message.reply_text.assert_called_once_with("سلام! 👋\nبه ربات خوش آمدید! لطفا یک گزینه را انتخاب کنید:")

def test_show_content(bot):
    # Simulate showing content
    update = MagicMock(spec=Update)
    update.callback_query.from_user.id = 1
    update.callback_query.answer = MagicMock()

    # Mock database interaction
    bot.db.get_user_page = MagicMock(return_value=1)
    bot.content_handler.get_page_content = MagicMock(return_value=Content("محتوای شماره 1", "این یک متن نمونه است"))

    bot.show_content(update, None)
    update.callback_query.answer.assert_called_once_with("📖 در حال نمایش محتوا...")
