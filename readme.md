# Telegram Retail Assistant Bot

**Bot Username:** [@tommyyiiee\_bot](https://t.me/tommyyiiee_bot)

## Description

This is a simple retail assistant Telegram bot built in Python using the `python-telegram-bot` library. It guides users through:

* Selecting a product category (e.g., Clothing, Electronics)
* Browsing 2–3 sample products in the chosen category
* Entering quantity and a delivery date (`dd-mm-yyyy`)
* Confirming the order
* Saving each confirmed order to a CSV file (`orders.csv`)

## Features

* `/start` command with category buttons
* Inline buttons for product selection
* Input validation for quantity and date format
* Order confirmation prompt
* CSV-based order logging with timestamp

## Prerequisites

* **Python 3.7+**
* A Telegram account and a bot token (from [@BotFather](https://t.me/BotFather))
* **python-telegram-bot** library (v20+)

## Installation

1. **Clone this repository**

   ```bash
   git clone <repo_url>
   cd <repo_folder>
   ```

2. **(Optional) Create and activate a virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install --upgrade python-telegram-bot
   ```

## Configuration

1. Rename your script to `telegram.py` (if it isn’t already).
2. In `telegram.py`, locate the token configuration:

   ```python
   app = ApplicationBuilder().token('YOUR_TELEGRAM_BOT_TOKEN').build()
   ```
3. Replace `'YOUR_TELEGRAM_BOT_TOKEN'` with your BotFather token. Alternatively, you can export an environment variable:

   ```bash
   export TELEGRAM_BOT_TOKEN="<your_token>"
   ```

   and modify the code to:

   ```python
   import os
   token = os.getenv('TELEGRAM_BOT_TOKEN')
   app = ApplicationBuilder().token(token).build()
   ```

## Running the Bot

Start the development server by running:

```bash
python3 telegram.py
```

The bot will connect to Telegram and begin polling for updates.

## Usage

1. Open Telegram and search for **@tommyyiiee\_bot**, or click the link above.
2. Send `/start` to begin placing an order.
3. Follow the on-screen prompts (category → product → quantity → date → confirm).

## Data Storage

All confirmed orders are appended to `orders.csv` in the project root. Columns:

```
user_id,category,product,quantity,delivery_date,created_at
```
