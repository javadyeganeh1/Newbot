import pytest
from unittest.mock import AsyncMock, MagicMock
from src.bot import TelegramBot

@pytest.fixture
def mock_bot():
    """ایجاد یک نمونه ماک از ربات برای تست"""
    bot = TelegramBot("TEST_TOKEN")
    bot.application.run_polling = MagicMock()  # جلوگیری از اجرای polling واقعی
    return bot

@pytest.mark.asyncio
async def test_start_command(mock_bot):
    """تست فرمان /start"""
    update = MagicMock()
    update.message.reply_text = AsyncMock()
    context = MagicMock()

    await mock_bot.start(update, context)
    update.message.reply_text.assert_called_once()  # بررسی ارسال پیام خوش‌آمدگویی

@pytest.mark.asyncio
async def test_show_content(mock_bot):
    """تست نمایش محتوا"""
    update = MagicMock()
    update.callback_query.answer = AsyncMock()
    update.callback_query.edit_message_text = AsyncMock()
    update.callback_query.from_user.id = 1234
    context = MagicMock()

    await mock_bot.show_content(update, context)
    update.callback_query.answer.assert_called_once()  # بررسی پاسخ به درخواست
    update.callback_query.edit_message_text.assert_called_once()  # بررسی ویرایش پیام

@pytest.mark.asyncio
async def test_handle_pagination(mock_bot):
    """تست دکمه‌های بعدی و قبلی"""
    update = MagicMock()
    update.callback_query.answer = AsyncMock()
    update.callback_query.from_user.id = 1234
    update.callback_query.data = "next_page"
    context = MagicMock()

    await mock_bot.handle_pagination(update, context)
    update.callback_query.answer.assert_called_once()  # بررسی تغییر صفحه

@pytest.mark.asyncio
async def test_add_favorite(mock_bot):
    """تست افزودن به علاقه‌مندی‌ها"""
    update = MagicMock()
    update.callback_query.answer = AsyncMock()
    update.callback_query.data = "add_favorite_1"
    update.callback_query.from_user.id = 1234
    context = MagicMock()

    await mock_bot.add_favorite(update, context)
    update.callback_query.answer.assert_called_once_with("✅ این محتوا به علاقه‌مندی‌های شما اضافه شد!")

@pytest.mark.asyncio
async def test_remove_favorite(mock_bot):
    """تست حذف از علاقه‌مندی‌ها"""
    update = MagicMock()
    update.callback_query.answer = AsyncMock()
    update.callback_query.data = "remove_favorite_1"
    update.callback_query.from_user.id = 1234
    context = MagicMock()

    await mock_bot.remove_favorite(update, context)
    update.callback_query.answer.assert_called_once_with("❌ این محتوا از علاقه‌مندی‌های شما حذف شد!")
