import os
import asyncio
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, JobQueue
from forex import ForexAnalyzer
from news import NewsAnalyzer
from alerts import AlertManager

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
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
        [InlineKeyboardButton("🔔 Set Alert", callback_data="set_alert"),
         InlineKeyboardButton("📈 Top Movers", callback_data="top_movers")],
        [InlineKeyboardButton("🌐 Session Status", callback_data="session_status"),
         InlineKeyboardButton("💡 AI Signal", callback_data="ai_signal")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    welcome_msg = """
🤖 *FOREX AI TRADING BOT* 🤖
━━━━━━━━━━━━━━━━━━━━━━

Welcome! Main tumhara *Advanced Forex Analyzer* hoon.

*Kya kar sakta hoon:*
• 📊 Real-time currency pair analysis
• 📰 Breaking forex news + sentiment
• ⚡ Economic events & high-impact news
• 🔔 Custom price alerts
• 💡 AI-powered trading signals
• 🌐 Live market session tracker

*Quick Commands:*
/analyze `EURUSD` - Pair analyze karo
/news - Latest forex news
/calendar - Economic calendar
/alert `EURUSD 1.0850` - Alert set karo
/pairs - Sabhi pairs
/signal `GBPUSD` - AI trading signal
/sessions - Market sessions

━━━━━━━━━━━━━━━━━━━━━━
_Powered by Groq AI + Live Data_
    """
    await update.message.reply_text(welcome_msg, parse_mode='Markdown', reply_markup=reply_markup)


async def analyze_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚠️ Usage: /analyze EURUSD\n\nExample pairs: EURUSD, GBPUSD, USDJPY, AUDUSD")
        return
    pair_input = context.args[0].upper()
    pair = pair_input[:3] + "/" + pair_input[3:] if "/" not in pair_input else pair_input
    msg = await update.message.reply_text(f"🔄 Analyzing {pair}... Please wait...")
    try:
        result = await forex.analyze_pair(pair)
        await msg.edit_text(result, parse_mode='Markdown')
    except Exception as e:
        await msg.edit_text(f"❌ Error: {str(e)}\nPlease try again.")


async def news_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = await update.message.reply_text("📰 Fetching latest forex news...")
    try:
        result = await news_analyzer.get_forex_news()
        await msg.edit_text(result, parse_mode='Markdown')
    except Exception as e:
        await msg.edit_text(f"❌ Error fetching news: {str(e)}")


async def calendar_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = await update.message.reply_text("⚡ Loading economic calendar...")
    try:
        result = await forex.get_economic_calendar()
        await msg.edit_text(result, parse_mode='Markdown')
    except Exception as e:
        await msg.edit_text(f"❌ Error: {str(e)}")


async def alert_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text(
            "⚠️ Usage: /alert EURUSD 1.0850\n\n"
            "Example:\n"
            "/alert EURUSD 1.0850\n"
            "/alert GBPUSD 1.2500"
        )
        return
    pair_input = context.args[0].upper()
    pair = pair_input[:3] + "/" + pair_input[3:] if "/" not in pair_input else pair_input
    try:
        target_price = float(context.args[1])
        user_id = update.effective_user.id
        alert_manager.add_alert(user_id, pair, target_price)
        await update.message.reply_text(
            f"✅ *Alert Set!*\n\n"
            f"💱 Pair: `{pair}`\n"
            f"🎯 Target: `{target_price}`\n\n"
            f"Main tumhe notify karunga jab price is level pe pahunche! 🔔",
            parse_mode='Markdown'
        )
    except ValueError:
        await update.message.reply_text("❌ Invalid price! Example: /alert EURUSD 1.0850")


async def pairs_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Major Pairs", callback_data="pairs_major")],
        [InlineKeyboardButton("Cross Pairs", callback_data="pairs_cross")],
        [InlineKeyboardButton("Exotic Pairs", callback_data="pairs_exotic")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("💱 *Select Pair Category:*", parse_mode='Markdown', reply_markup=reply_markup)


async def signal_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚠️ Usage: /signal EURUSD")
        return
    pair_input = context.args[0].upper()
    pair = pair_input[:3] + "/" + pair_input[3:] if "/" not in pair_input else pair_input
    msg = await update.message.reply_text(f"🤖 Generating AI signal for {pair}...")
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
        await query.edit_message_text("🔄 Loading market overview...")
        result = await forex.get_market_overview()
        await query.edit_message_text(result, parse_mode='Markdown')

    elif data == "latest_news":
        await query.edit_message_text("📰 Fetching news...")
        result = await news_analyzer.get_forex_news()
        await query.edit_message_text(result, parse_mode='Markdown')

    elif data == "choose_pair":
        keyboard = []
        for i in range(0, len(MAJOR_PAIRS), 2):
            row = []
            for pair in MAJOR_PAIRS[i:i+2]:
                symbol = pair.replace("/", "")
                row.append(InlineKeyboardButton(pair, callback_data=f"analyze_{symbol}"))
            keyboard.append(row)
        keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="back_main")])
        await query.edit_message_text(
            "💱 *Select a pair to analyze:*",
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data.startswith("analyze_"):
        symbol = data.replace("analyze_", "")
        pair = symbol[:3] + "/" + symbol[3:]
        await query.edit_message_text(f"🔄 Analyzing {pair}...")
        result = await forex.analyze_pair(pair)
        keyboard = [[InlineKeyboardButton("🔙 Back to Pairs", callback_data="choose_pair")]]
        await query.edit_message_text(result, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "economic_calendar":
        await query.edit_message_text("⚡ Loading economic calendar...")
        result = await forex.get_economic_calendar()
        await query.edit_message_text(result, parse_mode='Markdown')

    elif data == "top_movers":
        await query.edit_message_text("📈 Loading top movers...")
        result = await forex.get_top_movers()
        await query.edit_message_text(result, parse_mode='Markdown')

    elif data == "session_status":
        result = forex.get_session_status()
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="back_main")]]
        await query.edit_message_text(result, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "ai_signal":
        keyboard = []
        for i in range(0, len(MAJOR_PAIRS), 2):
            row = []
            for pair in MAJOR_PAIRS[i:i+2]:
                symbol = pair.replace("/", "")
                row.append(InlineKeyboardButton(pair, callback_data=f"signal_{symbol}"))
            keyboard.append(row)
        await query.edit_message_text(
            "💡 *Select pair for AI Signal:*",
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data.startswith("signal_"):
        symbol = data.replace("signal_", "")
        pair = symbol[:3] + "/" + symbol[3:]
        await query.edit_message_text(f"🤖 Generating AI signal for {pair}...")
        result = await forex.get_ai_signal(pair)
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="ai_signal")]]
        await query.edit_message_text(result, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith("pairs_"):
        category = data.replace("pairs_", "")
        pairs_map = {"major": MAJOR_PAIRS, "cross": CROSS_PAIRS, "exotic": EXOTIC_PAIRS}
        pairs = pairs_map.get(category, MAJOR_PAIRS)
        keyboard = []
        for i in range(0, len(pairs), 2):
            row = []
            for pair in pairs[i:i+2]:
                symbol = pair.replace("/", "")
                row.append(InlineKeyboardButton(pair, callback_data=f"analyze_{symbol}"))
            keyboard.append(row)
        keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="choose_pair")])
        await query.edit_message_text(
            f"💱 *{category.title()} Pairs:*",
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data == "back_main":
        keyboard = [
            [InlineKeyboardButton("📊 Market Overview", callback_data="market_overview"),
             InlineKeyboardButton("📰 Latest News", callback_data="latest_news")],
            [InlineKeyboardButton("🔍 Analyze Pair", callback_data="choose_pair"),
             InlineKeyboardButton("⚡ Economic Calendar", callback_data="economic_calendar")],
            [InlineKeyboardButton("🔔 Set Alert", callback_data="set_alert"),
             InlineKeyboardButton("📈 Top Movers", callback_data="top_movers")],
            [InlineKeyboardButton("🌐 Session Status", callback_data="session_status"),
             InlineKeyboardButton("💡 AI Signal", callback_data="ai_signal")]
        ]
        await query.edit_message_text(
            "🤖 *FOREX AI TRADING BOT*\n\nSelect an option:",
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


async def check_alerts_job(context: ContextTypes.DEFAULT_TYPE):
    try:
        alerts = alert_manager.get_all_alerts()
        for user_id, user_alerts in alerts.items():
            for alert in user_alerts:
                pair = alert['pair']
                target = alert['target']
                price_data = await forex.get_price(pair)
                if price_data:
                    current = price_data['price']
                    if abs(current - target) / target < 0.001:
                        await context.bot.send_message(
                            chat_id=user_id,
                            text=f"🔔 *ALERT TRIGGERED!*\n\n"
                                 f"💱 {pair}\n"
                                 f"🎯 Target: {target}\n"
                                 f"📍 Current: {current:.5f}\n\n"
                                 f"_Price has reached your target level!_",
                            parse_mode='Markdown'
                        )
                        alert_manager.remove_alert(user_id, pair, target)
    except Exception as e:
        logger.error(f"Alert check error: {e}")


def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("analyze", analyze_command))
    app.add_handler(CommandHandler("news", news_command))
    app.add_handler(CommandHandler("calendar", calendar_command))
    app.add_handler(CommandHandler("alert", alert_command))
    app.add_handler(CommandHandler("pairs", pairs_command))
    app.add_handler(CommandHandler("signal", signal_command))
    app.add_handler(CommandHandler("sessions", sessions_command))
    app.add_handler(CallbackQueryHandler(button_callback))
    job_queue = app.job_queue
    job_queue.run_repeating(check_alerts_job, interval=60, first=10)
    logger.info("🤖 Forex Bot is running...")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
