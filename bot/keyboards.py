from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from typing import List, Dict

class Keyboards:
    @staticmethod
    def admin_main_menu():
        """Main admin menu keyboard"""
        keyboard = [
            [InlineKeyboardButton("➕ Add Item", callback_data="admin_add_item")],
            [InlineKeyboardButton("👤 View Users", callback_data="admin_view_users")],
            [InlineKeyboardButton("💰 Manage Coins", callback_data="admin_manage_coins")],
            [InlineKeyboardButton("📦 View Orders", callback_data="admin_view_orders")],
            [InlineKeyboardButton("🏷️ Add Coupon", callback_data="admin_add_coupon")]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def user_main_menu():
        """Main user menu keyboard"""
        keyboard = [
            [InlineKeyboardButton("🛍️ Browse Items", callback_data="user_browse")],
            [InlineKeyboardButton("💰 My Balance", callback_data="user_balance")],
            [InlineKeyboardButton("📦 My Orders", callback_data="user_orders")]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def categories_menu(categories: List[str]):
        """Categories selection keyboard"""
        keyboard = []
        for category in categories:
            keyboard.append([InlineKeyboardButton(f"🎮 {category}", callback_data=f"category_{category}")])
        keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="back_to_main")])
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def items_menu(items: Dict, category: str):
        """Items in category keyboard"""
        keyboard = []
        for item_id, item in items.items():
            stock_text = f"({item['stock']} left)" if item['stock'] > 0 else "(Out of stock)"
            button_text = f"{item['name']} - {item['price']:,} MMK {stock_text}"
            keyboard.append([InlineKeyboardButton(button_text, callback_data=f"item_{item_id}")])
        
        keyboard.append([InlineKeyboardButton("🔙 Back to Categories", callback_data="back_to_categories")])
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def item_detail_menu(item_id: str, in_stock: bool):
        """Item detail keyboard"""
        keyboard = []
        if in_stock:
            keyboard.append([InlineKeyboardButton("💰 Buy Now", callback_data=f"buy_{item_id}")])
        keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="back_to_categories")])
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def users_list_menu(users: Dict):
        """Users list keyboard for admin"""
        keyboard = []
        for user_id, user in users.items():
            username = user.get('username', 'Unknown')
            coins = user.get('coins', 0)
            button_text = f"@{username} – {coins:,} MMK"
            keyboard.append([InlineKeyboardButton(button_text, callback_data=f"admin_user_{user_id}")])
        
        keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="back_to_admin")])
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def user_management_menu(user_id: str):
        """User management keyboard for admin"""
        keyboard = [
            [InlineKeyboardButton("➕ Add Coins", callback_data=f"admin_add_coins_{user_id}")],
            [InlineKeyboardButton("➖ Remove Coins", callback_data=f"admin_remove_coins_{user_id}")],
            [InlineKeyboardButton("🔙 Back", callback_data="admin_view_users")]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def orders_menu(orders: List[Dict]):
        """Orders management keyboard for admin"""
        keyboard = []
        for order in orders[:10]:  # Show max 10 orders
            order_id = order['order_id']
            user_id = order['user_id']
            keyboard.append([InlineKeyboardButton(f"Order {order_id}", callback_data=f"admin_order_{order_id}")])
        
        keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="back_to_admin")])
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def order_action_menu(order_id: str):
        """Order action keyboard for admin"""
        keyboard = [
            [InlineKeyboardButton("✅ Confirm", callback_data=f"admin_confirm_{order_id}")],
            [InlineKeyboardButton("❌ Reject", callback_data=f"admin_reject_{order_id}")],
            [InlineKeyboardButton("🔙 Back", callback_data="admin_view_orders")]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def purchase_confirmation_menu(item_id: str):
        """Purchase confirmation keyboard"""
        keyboard = [
            [InlineKeyboardButton("✅ Confirm Purchase", callback_data=f"confirm_buy_{item_id}")],
            [InlineKeyboardButton("🏷️ Use Coupon", callback_data=f"coupon_{item_id}")],
            [InlineKeyboardButton("❌ Cancel", callback_data="back_to_categories")]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def back_button():
        """Simple back button"""
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="back_to_main")]]
        return InlineKeyboardMarkup(keyboard)
