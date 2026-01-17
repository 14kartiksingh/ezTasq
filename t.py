from telegram.ext import Updater, CommandHandler
import json
from datetime import datetime

# 🔐 CONFIG
TOKEN = "5946547499:AAGq-EzZfjl-WUJP3C41EV0bq-NYyGbk4HU"
OWNER_ID = 1708011472  # <-- PUT YOUR TELEGRAM USER ID HERE
DATA_FILE = "expenses.json"

# ------------------ UTILS ------------------

def is_authorized(update):
    return update.message.from_user.id == OWNER_ID

def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# ------------------ COMMANDS ------------------

def start(update, context):
    if not is_authorized(update):
        update.message.reply_text("❌ Unauthorized access.")
        return

    update.message.reply_text(
        "💸 Private Expense Tracker\n\n"
        "/add amount category\n"
        "/list\n"
        "/total\n"
        "/daily\n"
        "/monthly\n"
        "/clear"
    )

def add(update, context):
    if not is_authorized(update):
        update.message.reply_text("❌ Unauthorized access.")
        return

    try:
        amount = float(context.args[0])
        category = context.args[1]

        data = load_data()
        data.append({
            "amount": amount,
            "category": category,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M")
        })
        save_data(data)

        update.message.reply_text(f"✅ Added ₹{amount} for {category}")
    except:
        update.message.reply_text("❌ Use: /add 100 food")

def list_expenses(update, context):
    if not is_authorized(update):
        update.message.reply_text("❌ Unauthorized access.")
        return

    data = load_data()
    if not data:
        update.message.reply_text("📭 No expenses yet.")
        return

    msg = "📋 Your Expenses:\n"
    for i, e in enumerate(data, 1):
        msg += f"{i}. ₹{e['amount']} - {e['category']} ({e['date']})\n"

    update.message.reply_text(msg)

def total(update, context):
    if not is_authorized(update):
        update.message.reply_text("❌ Unauthorized access.")
        return

    total_amt = sum(e["amount"] for e in load_data())
    update.message.reply_text(f"💰 Total Spent: ₹{total_amt}")

def daily(update, context):
    if not is_authorized(update):
        update.message.reply_text("❌ Unauthorized access.")
        return

    today = datetime.now().strftime("%Y-%m-%d")
    total = sum(
        e["amount"] for e in load_data()
        if e["date"].startswith(today)
    )

    update.message.reply_text(f"📅 Today’s Spend: ₹{total}")

def monthly(update, context):
    if not is_authorized(update):
        update.message.reply_text("❌ Unauthorized access.")
        return

    month = datetime.now().strftime("%Y-%m")
    total = sum(
        e["amount"] for e in load_data()
        if e["date"].startswith(month)
    )

    update.message.reply_text(f"📆 This Month’s Spend: ₹{total}")

def clear(update, context):
    if not is_authorized(update):
        update.message.reply_text("❌ Unauthorized access.")
        return

    save_data([])
    update.message.reply_text("🧹 All expenses cleared")

# ------------------ BOT START ------------------

updater = Updater(TOKEN, use_context=True)
dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("add", add))
dp.add_handler(CommandHandler("list", list_expenses))
dp.add_handler(CommandHandler("total", total))
dp.add_handler(CommandHandler("daily", daily))
dp.add_handler(CommandHandler("monthly", monthly))
dp.add_handler(CommandHandler("clear", clear))

print("🤖 Bot is running...")
updater.start_polling()
updater.idle()
