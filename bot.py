import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from forex import ForexAnalyzer
from news import NewsAnalyzer
from alerts import AlertManager

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "8792779625:AAEyyDTvoO1jTqgvha6GKvO2u64AwJGPFBw")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "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")

forex = ForexAnalyzer(GROQ_API_KEY)
news_analyzer = NewsAnalyzer(GROQ_API_KEY)
alert_manager = AlertManager()

MAJOR_PAIRS = ["EUR/USD", "GBP/USD", "USD/JPY", "USD/CHF", "AUD/USD", "USD/CAD", "NZD/USD"]
CROSS_PAIRS = ["EUR/GBP", "EUR/JPY", "GBP/JPY", "AUD/JPY", "EUR/AUD", "GBP/AUD"]
EXOTIC_PAIRS = ["USD/TRY", "USD/ZAR", "USD/MXN", "USD/SGD", "USD/HKD"]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📊 Market Overview", callback_data="market_overview"),
         InlineKeyboardButton("📰 Latest News", callback_data="latest_news")],
        [InlineKeyboardButton("🔍 Analyze Pair", callback_data="choose_pair"),
         InlineKeyboardButton("⚡ Economic Calendar", callback_data="economic_calendar")],
        [InlineKeyboardButton("📈 Top Movers", callback_data="top_movers"),
         InlineKeyboardButton("🌐 Session Status", callback_data="session_status")],
        [InlineKeyboardButton("💡 AI Signal", callback_data="ai_signal")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    welcome_msg = """
🤖 *FOREX AI TRADING BOT* 🤖
━━━━━━━━━━━━━━━━━━━━━━

Welcome! Main tumhara *Advanced Forex Analyzer* hoon.

*Quick Commands:*
/analyze EURUSD — Pair analyze karo
/news — Latest forex news
/calendar — Economic calendar
/alert EURUSD 1.0850 — Alert set karo
/signal GBPUSD — AI trading signal
/sessions — Market sessions

━━━━━━━━━━━━━━━━━━━━━━
_Powered by Groq AI_
"""
    await update.message.reply_text(welcome_msg, parse_mode='Markdown', reply_markup=reply_markup)


async def analyze_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚠️ Usage: /analyze EURUSD")
        return
    pair_input = context.args[0].upper()
    pair = pair_input[:3] + "/" + pair_input[3:] if "/" not in pair_input else pair_input
    msg = await update.message.reply_text(f"🔄 Analyzing {pair}...")
    try:
        result = await forex.analyze_pair(pair)
        await msg.edit_text(result, parse_mode='Markdown')
    except Exception as e:
        await msg.edit_text(f"❌ Error: {str(e)}")


async def news_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = await update.message.reply_text("📰 Fetching news...")
    try:
        result = await news_analyzer.get_forex_news()
        await msg.edit_text(result, parse_mode='Markdown')
    except Exception as e:
        await msg.edit_text(f"❌ Error: {str(e)}")


async def calendar_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = await update.message.reply_text("⚡ Loading calendar...")
    try:
        result = await forex.get_economic_calendar()
        await msg.edit_text(result, parse_mode='Markdown')
    except Exception as e:
        await msg.edit_text(f"❌ Error: {str(e)}")


async def alert_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("⚠️ Usage: /alert EURUSD 1.0850")
        return
    pair_input = context.args[0].upper()
    pair = pair_input[:3] + "/" + pair_input[3:] if "/" not in pair_input else pair_input
    try:
        target_price = float(context.args[1])
        user_id = update.effective_user.id
        alert_manager.add_alert(user_id, pair, target_price)
        await update.message.reply_text(
            f"✅ *Alert Set!*\n💱 Pair: `{pair}`\n🎯 Target: `{target_price}`",
            parse_mode='Markdown'
        )
    except ValueError:
        await update.message.reply_text("❌ Invalid price!")


async def signal_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚠️ Usage: /signal EURUSD")
        return
    pair_input = context.args[0].upper()
    pair = pair_input[:3] + "/" + pair_input[3:] if "/" not in pair_input else pair_input
    msg = await update.message.reply_text(f"🤖 Generating signal for {pair}...")
    try:
        result = await forex.get_ai_signal(pair)
        await msg.edit_text(result, parse_mode='Markdown')
    except Exception as e:
        await msg.edit_text(f"❌ Error: {str(e)}")


async def sessions_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = forex.get_session_status()
    await update.message.reply_text(result, parse_mode='Markdown')


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "market_overview":
        await query.edit_message_text("🔄 Loading...")
        result = await forex.get_market_overview()
        await query.edit_message_text(result, parse_mode='Markdown')

    elif data == "latest_news":
        await query.edit_message_text("📰 Fetching news...")
        result = await news_analyzer.get_forex_news()
        await query.edit_message_text(result, parse_mode='Markdown')

    elif data == "choose_pair":
        keyboard = []
        for i in range(0, len(MAJOR_PAIRS), 2):
            row = [InlineKeyboardButton(p, callback_data=f"analyze_{p.replace('/','')}")
                   for p in MAJOR_PAIRS[i:i+2]]
            keyboard.append(row)
        keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="back_main")])
        await query.edit_message_text("💱 *Select pair:*", parse_mode='Markdown',
                                       reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith("analyze_"):
        symbol = data.replace("analyze_", "")
        pair = symbol[:3] + "/" + symbol[3:]
        await query.edit_message_text(f"🔄 Analyzing {pair}...")
        result = await forex.analyze_pair(pair)
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="choose_pair")]]
        await query.edit_message_text(result, parse_mode='Markdown',
                                       reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "economic_calendar":
        await query.edit_message_text("⚡ Loading calendar...")
        result = await forex.get_economic_calendar()
        await query.edit_message_text(result, parse_mode='Markdown')

    elif data == "top_movers":
        await query.edit_message_text("📈 Loading...")
        result = await forex.get_top_movers()
        await query.edit_message_text(result, parse_mode='Markdown')

    elif data == "session_status":
        result = forex.get_session_status()
        await query.edit_message_text(result, parse_mode='Markdown')

    elif data == "ai_signal":
        keyboard = []
        for i in range(0, len(MAJOR_PAIRS), 2):
            row = [InlineKeyboardButton(p, callback_data=f"signal_{p.replace('/','')}")
                   for p in MAJOR_PAIRS[i:i+2]]
            keyboard.append(row)
        await query.edit_message_text("💡 *Select pair for signal:*", parse_mode='Markdown',
                                       reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith("signal_"):
        symbol = data.replace("signal_", "")
        pair = symbol[:3] + "/" + symbol[3:]
        await query.edit_message_text(f"🤖 Generating signal...")
        result = await forex.get_ai_signal(pair)
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="ai_signal")]]
        await query.edit_message_text(result, parse_mode='Markdown',
                                       reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "back_main":
        keyboard = [
            [InlineKeyboardButton("📊 Market Overview", callback_data="market_overview"),
             InlineKeyboardButton("📰 Latest News", callback_data="latest_news")],
            [InlineKeyboardButton("🔍 Analyze Pair", callback_data="choose_pair"),
             InlineKeyboardButton("⚡ Economic Calendar", callback_data="economic_calendar")],
            [InlineKeyboardButton("📈 Top Movers", callback_data="top_movers"),
             InlineKeyboardButton("🌐 Session Status", callback_data="session_status")],
            [InlineKeyboardButton("💡 AI Signal", callback_data="ai_signal")]
        ]
        await query.edit_message_text("🤖 *FOREX AI BOT*\nSelect option:",
                                       parse_mode='Markdown',
                                       reply_markup=InlineKeyboardMarkup(keyboard))


def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("analyze", analyze_command))
    app.add_handler(CommandHandler("news", news_command))
    app.add_handler(CommandHandler("calendar", calendar_command))
    app.add_handler(CommandHandler("alert", alert_command))
    app.add_handler(CommandHandler("signal", signal_command))
    app.add_handler(CommandHandler("sessions", sessions_command))
    app.add_handler(CallbackQueryHandler(button_callback))
    logger.info("🤖 Bot starting...")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
