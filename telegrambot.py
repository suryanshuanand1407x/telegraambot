import logging
import os
import csv
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler, MessageHandler, filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

CATEGORIES ={
    'Clothing': ['T-Shirt', 'Jeans', 'Jacket'],
    'Electronics': ['Smartphone', 'Laptop', 'Headphones']
}
CSV_FILE = 'orders.csv'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message with category buttons on /start."""
    keyboard = [[InlineKeyboardButton(cat, callback_data=f'category_{cat}')] for cat in CATEGORIES]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Welcome! Please choose a category:', reply_markup=reply_markup)

async def category_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle category selection and show products."""
    query = update.callback_query
    await query.answer()
    category = query.data.split('_', 1)[1]
    context.user_data['category'] = category
    keyboard = [[InlineKeyboardButton(item, callback_data=f'product_{item}')] for item in CATEGORIES[category]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(f'Category: {category}\nSelect a product:', reply_markup=reply_markup)

async def product_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle product selection and ask for quantity."""
    query = update.callback_query
    await query.answer()
    product = query.data.split('_', 1)[1]
    context.user_data['product'] = product
    context.user_data['state'] = 'quantity'
    await query.edit_message_text(f'Product: {product}\nPlease enter the quantity:')

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle messages for quantity, date, and other states."""
    state = context.user_data.get('state')
    text = update.message.text.strip()

    if state == 'quantity':
        if not text.isdigit():
            await update.message.reply_text('Quantity must be a number. Please enter again:')
            return
        context.user_data['quantity'] = text
        context.user_data['state'] = 'date'
        await update.message.reply_text('Please enter delivery date (dd-mm-yyyy):')

    elif state == 'date':
        try:
            delivery = datetime.strptime(text, '%d-%m-%Y').date()
        except ValueError:
            await update.message.reply_text('Invalid date format. Use dd-mm-yyyy:')
            return
        context.user_data['delivery_date'] = delivery.strftime('%d-%m-%Y')

        summary = (
            f"Category: {context.user_data['category']}\n"
            f"Product: {context.user_data['product']}\n"
            f"Quantity: {context.user_data['quantity']}\n"
            f"Delivery Date: {context.user_data['delivery_date']}"
        )
        keyboard = [
            [InlineKeyboardButton('Confirm', callback_data='confirm_yes'),
             InlineKeyboardButton('Cancel', callback_data='confirm_no')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.user_data['state'] = 'confirm'
        await update.message.reply_text(f'Please confirm your order:\n{summary}', reply_markup=reply_markup)

    else:
        await update.message.reply_text('Please use /start to begin your order.')

async def confirm_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle order confirmation and save to CSV."""
    query = update.callback_query
    await query.answer()
    choice = query.data.split('_', 1)[1]

    if choice == 'yes':
        user_id = query.from_user.id
        row = [
            user_id,
            context.user_data['category'],
            context.user_data['product'],
            context.user_data['quantity'],
            context.user_data['delivery_date'],
            datetime.now().isoformat()
        ]
        save_order(row)
        await query.edit_message_text('✅ Thank you! Your order has been confirmed.')
    else:
        await query.edit_message_text('❌ Your order has been canceled.')

    context.user_data.clear()

def save_order(data: list) -> None:
    """Append order data to CSV, creating file with header if needed."""
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(['user_id', 'category', 'product', 'quantity', 'delivery_date', 'created_at'])
        writer.writerow(data)


if __name__ == '__main__':
    app = ApplicationBuilder().token('8029353345:AAG20sbMzE7xGcwx5dxN7wRbvW6dLmzNip8').build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(CallbackQueryHandler(category_handler, pattern='^category_'))
    app.add_handler(CallbackQueryHandler(product_handler, pattern='^product_'))
    app.add_handler(CallbackQueryHandler(confirm_handler, pattern='^confirm_'))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    app.run_polling()
