import os
import logging
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from bot.handlers.user_handlers import UserHandlers
from bot.handlers.admin_handlers import AdminHandlers
from bot.database import Database
from bot.utils import is_admin

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot token from environment
BOT_TOKEN = os.getenv('BOT_TOKEN', '8148103685:AAHY3QnChU0qsii8SlETfDjTJwKcQSdpF6Q')
OWNER_ID = int(os.getenv('OWNER_ID', '1735522859'))

class TelegramBot:
    def __init__(self):
        self.database = Database()
        self.user_handlers = UserHandlers(self.database)
        self.admin_handlers = AdminHandlers(self.database)
        
    async def start_command(self, update, context):
        """Handle /start command - shows different menus for admin vs user"""
        user_id = update.effective_user.id
        username = update.effective_user.username or "Unknown"
        
        # Register user if not exists
        self.database.register_user(user_id, username)
        
        # Send welcome message
        welcome_text = f"🎮 Welcome to @{username}\n\n🏪Osamu Gaming Items Store!🏪\n\nSelect an option:"
        
        if is_admin(user_id):
            await update.message.reply_text(
                welcome_text,
                reply_markup=self.admin_handlers.keyboards.admin_main_menu()
            )
        else:
            await update.message.reply_text(
                welcome_text,
                reply_markup=self.user_handlers.keyboards.user_main_menu()
            )
    
    async def handle_callback(self, update, context):
        """Route callback queries to appropriate handlers"""
        query = update.callback_query
        await query.answer()
        
        data = query.data
        user_id = query.from_user.id
        
        # Admin callbacks
        if is_admin(user_id) and data.startswith('admin_'):
            await self.admin_handlers.handle_callback(update, context)
        # User callbacks
        elif data.startswith('user_') or data.startswith('category_') or data.startswith('item_') or data.startswith('buy_') or data.startswith('coupon_'):
            await self.user_handlers.handle_callback(update, context)
        # Back buttons and general navigation
        elif data in ['back_to_main', 'back_to_admin', 'back_to_categories']:
            if is_admin(user_id) and data == 'back_to_admin':
                await self.admin_handlers.show_admin_menu(update, context)
            elif data == 'back_to_main':
                if is_admin(user_id):
                    await self.admin_handlers.show_admin_menu(update, context)
                else:
                    await self.user_handlers.show_user_menu(update, context)
            elif data == 'back_to_categories':
                await self.user_handlers.show_categories(update, context)
    
    async def handle_message(self, update, context):
        """Handle text messages based on current state"""
        user_id = update.effective_user.id
        
        if is_admin(user_id):
            await self.admin_handlers.handle_message(update, context)
        else:
            await self.user_handlers.handle_message(update, context)
    
    def run(self):
        """Start the bot"""
        application = Application.builder().token(BOT_TOKEN).build()
        
        # Handlers
        application.add_handler(CommandHandler("start", self.start_command))
        application.add_handler(CallbackQueryHandler(self.handle_callback))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        
        # Start polling
        print("Bot starting...")
        application.run_polling(allowed_updates=['message', 'callback_query'])

if __name__ == '__main__':
    bot = TelegramBot()
    bot.run()
