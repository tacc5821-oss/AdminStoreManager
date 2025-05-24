import os
import asyncio
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Bot configuration
BOT_TOKEN = os.getenv('BOT_TOKEN', '8148103685:AAHY3QnChU0qsii8SlETfDjTJwKcQSdpF6Q')
OWNER_ID = int(os.getenv('OWNER_ID', '1735522859'))

class TelegramBot:
    def __init__(self):
        pass
    
    def is_admin(self, user_id: int) -> bool:
        """Check if user is admin"""
        return user_id == OWNER_ID
    
    def get_user_keyboard(self):
        """Get user keyboard"""
        keyboard = [
            [KeyboardButton("🛍️ Browse Items"), KeyboardButton("💰 My Balance")],
            [KeyboardButton("📦 My Orders")]
        ]
        return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
    
    def get_admin_keyboard(self):
        """Get admin keyboard"""
        keyboard = [
            [KeyboardButton("➕ Add Item"), KeyboardButton("📝 Manage Items")],
            [KeyboardButton("👤 View Users"), KeyboardButton("💰 Manage Coins")],
            [KeyboardButton("📦 View Orders"), KeyboardButton("🏷️ Add Coupon")],
            [KeyboardButton("🎫 Manage Coupons")]
        ]
        return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user_id = update.effective_user.id
        username = update.effective_user.username or "User"
        
        welcome_text = f"🎮 Welcome to @{username}\n\n🏪Osamu Gaming Items Store!🏪\n\nSelect an option:"
        
        if self.is_admin(user_id):
            await update.message.reply_text(
                welcome_text,
                reply_markup=self.get_admin_keyboard()
            )
        else:
            await update.message.reply_text(
                welcome_text,
                reply_markup=self.get_user_keyboard()
            )
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle text messages"""
        user_id = update.effective_user.id
        text = update.message.text
        
        if self.is_admin(user_id):
            # Handle admin buttons
            if text == "➕ Add Item":
                await update.message.reply_text("🎯 Add Item feature coming soon!")
            elif text == "📝 Manage Items":
                await update.message.reply_text("🔧 Manage Items feature coming soon!")
            elif text == "👤 View Users":
                await update.message.reply_text("👥 View Users feature coming soon!")
            elif text == "💰 Manage Coins":
                await update.message.reply_text("💰 Manage Coins feature coming soon!")
            elif text == "📦 View Orders":
                await update.message.reply_text("📋 View Orders feature coming soon!")
            elif text == "🏷️ Add Coupon":
                await update.message.reply_text("🎫 Add Coupon feature coming soon!")
            elif text == "🎫 Manage Coupons":
                await update.message.reply_text("🎪 Manage Coupons feature coming soon!")
            else:
                await update.message.reply_text("Please use the menu buttons or type /start")
        else:
            # Handle user buttons
            if text == "🛍️ Browse Items":
                await update.message.reply_text("🛒 Browse Items feature coming soon!")
            elif text == "💰 My Balance":
                await update.message.reply_text("💳 Your Balance: 0 MMK")
            elif text == "📦 My Orders":
                await update.message.reply_text("📦 You have no orders yet.")
            else:
                await update.message.reply_text("Please use the menu buttons or type /start")
    
    def run(self):
        """Start the bot"""
        print("Bot starting...")
        application = Application.builder().token(BOT_TOKEN).build()
        
        # Add handlers
        application.add_handler(CommandHandler("start", self.start_command))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        
        # Start the bot
        application.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    bot = TelegramBot()
    bot.run()