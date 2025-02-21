"""
Main bot module for handling Telegram interactions.
"""
from typing import Optional
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext
from database import DatabaseManager
from content import ContentRepository, Content

class ContentHandler:
    """Class responsible for handling content-related actions."""
    def __init__(self, content_repo: ContentRepository, db: DatabaseManager):
        self.content_repo = content_repo
        self.db = db

    def get_page_content(self, page: int) -> Optional[Content]:
        """Get content for the specified page"""
        if 1 <= page <= self.content_repo.total_pages:
            return self.content_repo.content[page - 1]
        return None

    def create_content_keyboard(self, user_id: int, page: int) -> InlineKeyboardMarkup:
        """Create keyboard for content navigation"""
        is_favorite = page in self.db.get_favorites(user_id)
        favorite_button = (
            "💔 حذف از علاقه‌مندی‌ها" if is_favorite else "❤️ افزودن به علاقه‌مندی‌ها"
        )
        favorite_action = f"remove_favorite_{page}" if is_favorite else f"add_favorite_{page}"

        buttons = [
            [
                InlineKeyboardButton("⬅️ قبلی", callback_data="prev_page"),
                InlineKeyboardButton(
                    f"{page}/{self.content_repo.total_pages}", callback_data="noop"
                ),
                InlineKeyboardButton("➡️ بعدی", callback_data="next_page"),
            ],
            [InlineKeyboardButton(favorite_button, callback_data=favorite_action)],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="back")],
        ]
        return InlineKeyboardMarkup(buttons)

class TelegramBot:
    """Main bot class handling Telegram interactions"""
    def __init__(self, token: str):
        self.application = Application.builder().token(token).build()
        self.db = DatabaseManager()
        self.content_handler = ContentHandler(ContentRepository(), self.db)
        self._register_handlers()

    def _register_handlers(self):
        """Register all command and callback handlers"""
        handlers = [
            CommandHandler("start", self.start),
            CallbackQueryHandler(self.show_content, pattern="show_content"),
            CallbackQueryHandler(self.handle_pagination, pattern="prev_page|next_page"),
            CallbackQueryHandler(self.add_favorite, pattern=r"^add_favorite_\d+$"),
            CallbackQueryHandler(self.remove_favorite, pattern=r"^remove_favorite_\d+$"),
            CallbackQueryHandler(self.show_favorites, pattern="show_favorites"),
            CallbackQueryHandler(self.handle_back, pattern="back"),
            CommandHandler("search", self.search_content)
        ]
        for handler in handlers:
            self.application.add_handler(handler)

    async def start(self, update: Update, context: CallbackContext):
        """Show main menu"""
        keyboard = [
            [InlineKeyboardButton("📖 نمایش محتوا", callback_data="show_content")],
            [InlineKeyboardButton("🔍 جستجو", callback_data="search")],
            [InlineKeyboardButton("❤️ علاقه‌مندی‌ها", callback_data="show_favorites")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "سلام! 👋\nبه ربات خوش آمدید! لطفا یک گزینه را انتخاب کنید:",
            reply_markup=reply_markup,
        )

    async def show_content(self, update: Update, context: CallbackContext):
        """Show content for current page"""
        query = update.callback_query
        user_id = query.from_user.id
        await query.answer("📖 در حال نمایش محتوا...")

        page = self.db.get_user_page(user_id)
        content = self.content_handler.get_page_content(page)

        if not content:
            await query.answer("🚫 صفحه‌ای برای نمایش وجود ندارد.")
            return

        keyboard = self.content_handler.create_content_keyboard(user_id, page)
        await query.edit_message_text(
            text=self._format_content(content),
            reply_markup=keyboard,
            parse_mode="MarkdownV2",
        )

    async def search_content(self, update: Update, context: CallbackContext):
        """Handle search requests"""
        query = update.message.text.split(' ', 1)
        if len(query) < 2:
            await update.message.reply_text("لطفا یک کلمه برای جستجو وارد کنید.")
            return

        search_term = query[1]
        results = [content for content in self.content_repo.content if search_term.lower() in content.title.lower()]

        if not results:
            await update.message.reply_text("هیچ نتیجه‌ای پیدا نشد.")
            return

        result_buttons = [
            [InlineKeyboardButton(content.title, callback_data=f"show_result_{index}")]
            for index, content in enumerate(results)
        ]
        
        await update.message.reply_text(
            "نتایج جستجو:",
            reply_markup=InlineKeyboardMarkup(result_buttons)
        )

    def _format_content(self, content: Content) -> str:
        """Format content for Telegram message"""
        return f"*{content.title}*\n\n_{content.text}_"

    async def handle_pagination(self, update: Update, context: CallbackContext):
        """Handle pagination navigation"""
        query = update.callback_query
        user_id = query.from_user.id
        await query.answer("⏳ در حال تغییر صفحه...")

        current_page = self.db.get_user_page(user_id)
        new_page = current_page

        if query.data == "next_page" and current_page < self.content_repo.total_pages:
            new_page += 1
        elif query.data == "prev_page" and current_page > 1:
            new_page -= 1
        else:
            await query.answer("🚫 صفحه‌ای برای نمایش وجود ندارد.")
            return

        self.db.set_user_page(user_id, new_page)
        await self.show_content(update, context)

    async def add_favorite(self, update: Update, context: CallbackContext):
        """Add current page to favorites"""
        query = update.callback_query
        user_id = query.from_user.id
        page = int(query.data.split("_")[-1])

        self.db.add_favorite(user_id, page)
        await query.answer("✅ این محتوا به علاقه‌مندی‌های شما اضافه شد!")

    async def remove_favorite(self, update: Update, context: CallbackContext):
        """Remove current page from favorites"""
        query = update.callback_query
        user_id = query.from_user.id
        page = int(query.data.split("_")[-1])

        self.db.remove_favorite(user_id, page)
        await query.answer("❌ این محتوا از علاقه‌مندی‌های شما حذف شد!")

    async def show_favorites(self, update: Update, context: CallbackContext):
        """Show user's favorite items"""
        query = update.callback_query
        user_id = query.from_user.id
        await query.answer("❤️ در حال بارگذاری علاقه‌مندی‌ها...")

        favorite_pages = self.db.get_favorites(user_id)
        content_items = [
            self.content_handler.get_page_content(page) for page in favorite_pages
        ]
        valid_items = [item for item in content_items if item]

        if not valid_items:
            await query.edit_message_text(
                text="🚫 شما هیچ علاقه‌مندی ندارید.",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("🔙 بازگشت", callback_data="back")]]
                ),
            )
            return

        keyboard = [
            [InlineKeyboardButton(item.title, callback_data=f"show_result_{index}")]
            for index, item in enumerate(valid_items)
        ]
        await query.edit_message_text(
            text="📌 علاقه‌مندی‌های شما:",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    async def handle_back(self, update: Update, context: CallbackContext):
        """Handle back to main menu"""
        query = update.callback_query
        await self.start(query, context)

    def run(self):
        """Start the bot"""
        self.application.run_polling()
if __name__ == "__main__":
        # Load token from environment variable for security
        TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_BOT_TOKEN")
        
        # Initialize and run the bot
        bot = TelegramBot(TOKEN)
        bot.run()
