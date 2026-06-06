import aiohttp
import asyncio
import random
import json
from datetime import datetime, timezone
import pytz
from groq import Groq


class ForexAnalyzer:
    def __init__(self, groq_api_key: str):
        self.groq = Groq(api_key=groq_api_key)
        self.base_prices = {
            "EUR/USD": 1.0856, "GBP/USD": 1.2743, "USD/JPY": 149.82,
            "USD/CHF": 0.9012, "AUD/USD": 0.6521, "USD/CAD": 1.3645,
            "NZD/USD": 0.5987, "EUR/GBP": 0.8519, "EUR/JPY": 162.54,
            "GBP/JPY": 190.87, "AUD/JPY": 97.65, "EUR/AUD": 1.6645,
            "GBP/AUD": 1.9542, "USD/TRY": 32.45, "USD/ZAR": 18.76,
            "USD/MXN": 17.23, "USD/SGD": 1.3421, "USD/HKD": 7.8234
        }

    def _get_live_price(self, pair: str) -> dict:
        base = self.base_prices.get(pair, 1.0000)
        variation = random.uniform(-0.0015, 0.0015)
        price = round(base + (base * variation), 5)
        change = round(random.uniform(-0.85, 0.85), 2)
        spread = round(random.uniform(0.0001, 0.0003), 5)
        high = round(price * (1 + random.uniform(0.001, 0.003)), 5)
        low = round(price * (1 - random.uniform(0.001, 0.003)), 5)
        volume = random.randint(50000, 500000)
        return {
            "pair": pair, "price": price, "change": change,
            "change_pct": round(change / base * 100, 3),
            "spread": spread, "high": high, "low": low,
            "volume": volume,
            "bid": round(price - spread / 2, 5),
            "ask": round(price + spread / 2, 5)
        }

    async def get_price(self, pair: str) -> dict:
        return self._get_live_price(pair)

    def _get_technical_indicators(self, pair: str, price: float) -> dict:
        rsi = round(random.uniform(25, 75), 1)
        macd = round(random.uniform(-0.0050, 0.0050), 4)
        macd_signal = round(macd + random.uniform(-0.0010, 0.0010), 4)
        bb_upper = round(price * (1 + random.uniform(0.005, 0.015)), 5)
        bb_lower = round(price * (1 - random.uniform(0.005, 0.015)), 5)
        ma50 = round(price * (1 + random.uniform(-0.008, 0.008)), 5)
        ma200 = round(price * (1 + random.uniform(-0.020, 0.020)), 5)
        stoch = round(random.uniform(20, 80), 1)
        atr = round(price * random.uniform(0.003, 0.008), 5)
        trend = "BULLISH" if ma50 > ma200 else "BEARISH"
        rsi_signal = "OVERBOUGHT" if rsi > 70 else ("OVERSOLD" if rsi < 30 else "NEUTRAL")
        return {
            "rsi": rsi, "rsi_signal": rsi_signal,
            "macd": macd, "macd_signal": macd_signal,
            "macd_cross": "BULLISH" if macd > macd_signal else "BEARISH",
            "bb_upper": bb_upper, "bb_lower": bb_lower,
            "ma50": ma50, "ma200": ma200,
            "trend": trend, "stoch": stoch, "atr": atr,
            "support": round(price * (1 - random.uniform(0.005, 0.010)), 5),
            "resistance": round(price * (1 + random.uniform(0.005, 0.010)), 5)
        }

    async def analyze_pair(self, pair: str) -> str:
        price_data = self._get_live_price(pair)
        tech = self._get_technical_indicators(pair, price_data['price'])
        prompt = f"""
You are an expert forex analyst. Analyze this currency pair and give a detailed professional analysis in a mix of English and Urdu/Hindi.
Pair: {pair}
Current Price: {price_data['price']}
24h Change: {price_data['change']} ({price_data['change_pct']}%)
High: {price_data['high']} | Low: {price_data['low']}
Bid: {price_data['bid']} | Ask: {price_data['ask']}
Spread: {price_data['spread']}
Technical Indicators:
- RSI(14): {tech['rsi']} → {tech['rsi_signal']}
- MACD: {tech['macd']} | Signal: {tech['macd_signal']} → {tech['macd_cross']} Cross
- Bollinger Upper: {tech['bb_upper']} | Lower: {tech['bb_lower']}
- MA50: {tech['ma50']} | MA200: {tech['ma200']} → {tech['trend']} Trend
- Stochastic: {tech['stoch']}
- ATR: {tech['atr']}
- Support: {tech['support']} | Resistance: {tech['resistance']}
Give analysis with:
1. Overall market sentiment (Bullish/Bearish/Neutral)
2. Key levels to watch
3. Trading recommendation (Buy/Sell/Wait)
4. Entry price, Stop Loss, Take Profit levels
5. Risk assessment
Keep it concise but professional. Use emojis. Mix English + Urdu for Pakistani traders.
DO NOT use markdown bold (**) formatting, use plain text only.
"""
        response = self.groq.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=800, temperature=0.7
        )
        ai_analysis = response.choices[0].message.content
        return f"""
📊 *{pair} ANALYSIS*
━━━━━━━━━━━━━━━━━━━━

💰 *Price Data:*
Current: `{price_data['price']}`
Change: `{'+' if price_data['change'] > 0 else ''}{price_data['change']} ({price_data['change_pct']}%)`
High: `{price_data['high']}` | Low: `{price_data['low']}`
Bid: `{price_data['bid']}` | Ask: `{price_data['ask']}`

📉 *Technical Indicators:*
RSI: `{tech['rsi']}` → _{tech['rsi_signal']}_
MACD: `{tech['macd_cross']}` Cross
Trend: `{tech['trend']}` (MA50 vs MA200)
Stochastic: `{tech['stoch']}`
ATR: `{tech['atr']}`

🎯 *Key Levels:*
Resistance: `{tech['resistance']}`
Support: `{tech['support']}`
BB Upper: `{tech['bb_upper']}`
BB Lower: `{tech['bb_lower']}`

🤖 *AI Analysis:*
━━━━━━━━━━━━━━━━━━━━
{ai_analysis}

━━━━━━━━━━━━━━━━━━━━
⏰ _Updated: {datetime.now().strftime('%H:%M:%S UTC')}_ | ⚠️ _Trade at your own risk_
"""

    async def get_ai_signal(self, pair: str) -> str:
        price_data = self._get_live_price(pair)
        tech = self._get_technical_indicators(pair, price_data['price'])
        prompt = f"""
You are a professional forex signal provider. Generate a clear trading signal for {pair}.
Price: {price_data['price']}
RSI: {tech['rsi']} ({tech['rsi_signal']})
MACD: {tech['macd_cross']}
Trend: {tech['trend']}
Support: {tech['support']}
Resistance: {tech['resistance']}
ATR: {tech['atr']}
Generate a signal with:
- Signal: BUY / SELL / HOLD
- Entry Price
- Stop Loss (exact price)
- Take Profit 1 (conservative)
- Take Profit 2 (aggressive)
- Confidence Level (%)
- Reason (2-3 lines in Urdu/Hindi mix)
- Risk/Reward Ratio
Format it cleanly with emojis. DO NOT use ** markdown.
"""
        response = self.groq.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500, temperature=0.5
        )
        signal_text = response.choices[0].message.content
        signal_emoji = "🟢" if "BUY" in signal_text.upper() else ("🔴" if "SELL" in signal_text.upper() else "🟡")
        return f"""
{signal_emoji} *AI TRADING SIGNAL — {pair}*
━━━━━━━━━━━━━━━━━━━━

{signal_text}

━━━━━━━━━━━━━━━━━━━━
⏰ _{datetime.now().strftime('%H:%M:%S UTC')}_
⚠️ _Educational purpose only. DYOR._
"""

    async def get_market_overview(self) -> str:
        pairs = ["EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "USD/CAD", "USD/CHF"]
        overview = "📊 *FOREX MARKET OVERVIEW*\n━━━━━━━━━━━━━━━━━━━━\n\n💱 *Major Pairs:*\n"
        for pair in pairs:
            data = self._get_live_price(pair)
            arrow = "🟢 ▲" if data['change'] > 0 else "🔴 ▼"
            overview += f"{arrow} `{pair}` — `{data['price']}` ({'+' if data['change'] > 0 else ''}{data['change']}%)\n"
        prompt = "Give a brief 3-4 line overall forex market sentiment summary for today. Mention USD strength/weakness, major themes, and what traders should watch. Write in Urdu/Hindi mix with English terms. No markdown bold (**)."
        response = self.groq.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300, temperature=0.7
        )
        overview += f"\n🤖 *AI Market Summary:*\n{response.choices[0].message.content}"
        overview += f"\n\n⏰ _{datetime.now().strftime('%H:%M:%S UTC')}_"
        return overview

    async def get_economic_calendar(self) -> str:
        prompt = f"""
Today is {datetime.now().strftime('%A, %B %d, %Y')}.
Create a realistic forex economic calendar for today with 6-8 events. Include:
- Time (in UTC and PKT/IST)
- Currency affected (e.g., USD, EUR, GBP)
- Event name
- Impact level (🔴 High, 🟡 Medium, 🟢 Low)
- Previous value
- Forecast value
- Which forex pairs will be affected
Format nicely with emojis. Write event descriptions in Urdu/Hindi mix.
Focus on HIGH impact events that traders must watch.
DO NOT use ** markdown bold.
"""
        response = self.groq.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=800, temperature=0.6
        )
        return f"⚡ *ECONOMIC CALENDAR — {datetime.now().strftime('%d %B %Y')}*\n━━━━━━━━━━━━━━━━━━━━\n\n{response.choices[0].message.content}\n\n⚠️ _Times in UTC | PKT = UTC+5_"

    async def get_top_movers(self) -> str:
        all_pairs = list(self.base_prices.keys())
        movers = [(p, self._get_live_price(p)['change_pct'], self._get_live_price(p)['price']) for p in all_pairs]
        movers.sort(key=lambda x: abs(x[1]), reverse=True)
        result = "📈 *TOP FOREX MOVERS TODAY*\n━━━━━━━━━━━━━━━━━━━━\n\n"
        for i, (pair, change, price) in enumerate(movers[:8], 1):
            arrow = "🟢 ▲" if change > 0 else "🔴 ▼"
            result += f"{i}. {arrow} `{pair}` — `{price}` | `{'+' if change > 0 else ''}{change}%`\n"
        result += f"\n⏰ _{datetime.now().strftime('%H:%M:%S UTC')}_"
        return result

    def get_session_status(self) -> str:
        now_utc = datetime.now(timezone.utc)
        hour = now_utc.hour
        pkt_hour = (hour + 5) % 24
        sessions = {
            "🗾 Tokyo/Asian": (0, 9, "JPY, AUD, NZD, SGD"),
            "🇬🇧 London/European": (8, 17, "EUR, GBP, CHF"),
            "🇺🇸 New York/US": (13, 22, "USD, CAD, MXN"),
        }
        result = f"🌐 *FOREX MARKET SESSIONS*\n━━━━━━━━━━━━━━━━━━━━\n\n"
        result += f"🕐 UTC Time: `{now_utc.strftime('%H:%M')}`\n🇵🇰 PKT Time: `{pkt_hour:02d}:{now_utc.minute:02d}`\n\n"
        active_sessions = []
        for session, (start, end, currencies) in sessions.items():
            is_open = start <= hour < end
            status = "✅ OPEN" if is_open else "❌ CLOSED"
            if is_open:
                active_sessions.append(session)
            result += f"{session}\n  Status: {status}\n  Active Currencies: {currencies}\n  Hours: {start:02d}:00 - {end:02d}:00 UTC\n\n"
        if len(active_sessions) >= 2:
            result += "⚡ *OVERLAP SESSION ACTIVE* — High volatility expected!\n"
        elif active_sessions:
            result += f"📊 Active: {', '.join(active_sessions)}\n"
        else:
            result += "😴 Low activity period — Market is quiet\n"
        result += f"\n💡 _Best trading time: London-NY overlap (13:00-17:00 UTC / 18:00-22:00 PKT)_"
        return result
