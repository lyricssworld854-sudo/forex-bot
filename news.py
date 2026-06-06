import aiohttp
import asyncio
from datetime import datetime
from groq import Groq
import xml.etree.ElementTree as ET


class NewsAnalyzer:
    def __init__(self, groq_api_key: str):
        self.groq = Groq(api_key=groq_api_key)
        self.rss_feeds = [
            "https://feeds.reuters.com/reuters/businessNews",
            "https://www.forexlive.com/feed/",
            "https://www.dailyfx.com/feeds/market-news",
        ]

    async def fetch_rss(self, url: str) -> list:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=8)) as resp:
                    if resp.status == 200:
                        text = await resp.text()
                        root = ET.fromstring(text)
                        items = []
                        for item in root.iter('item'):
                            title = item.find('title')
                            desc = item.find('description')
                            pub_date = item.find('pubDate')
                            if title is not None:
                                items.append({
                                    'title': title.text or '',
                                    'desc': desc.text[:200] if desc is not None and desc.text else '',
                                    'date': pub_date.text if pub_date is not None else ''
                                })
                        return items[:5]
        except Exception:
            return []

    async def get_forex_news(self) -> str:
        prompt = f"""
Today is {datetime.now().strftime('%A, %B %d, %Y at %H:%M UTC')}.

Generate 6 realistic forex market news headlines for today. For each news item include:
- Headline (realistic and specific)
- Affected currency pairs
- Market impact (Bullish/Bearish for which currency)
- Brief explanation (2 lines in Urdu/Hindi mix)
- Sentiment: 🟢 Positive / 🔴 Negative / 🟡 Neutral for USD

Make it realistic like actual forex news. Include mentions of:
- Fed/Central bank decisions or hints
- Economic data releases  
- Geopolitical events affecting forex
- Commodity prices (Oil, Gold affecting CAD, AUD)

DO NOT use ** markdown bold. Use emojis generously.
"""
        response = self.groq.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=900,
            temperature=0.8
        )
        news_content = response.choices[0].message.content
        sentiment_prompt = f"""
Based on this forex news summary, give overall market sentiment in 2 lines:
{news_content[:500]}
Format: Overall sentiment for USD today + what traders should do.
In Urdu/Hindi mix. No markdown.
"""
        sentiment_response = self.groq.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": sentiment_prompt}],
            max_tokens=150,
            temperature=0.5
        )
        result = f"""
📰 *FOREX NEWS & SENTIMENT*
━━━━━━━━━━━━━━━━━━━━
📅 {datetime.now().strftime('%d %B %Y | %H:%M UTC')}
🇵🇰 PKT: {datetime.now().strftime('%H:%M')} +5

{news_content}

━━━━━━━━━━━━━━━━━━━━
🎯 *Overall Sentiment:*
{sentiment_response.choices[0].message.content}

⚠️ _News is AI-generated for educational purposes. Always verify before trading._
"""
        return result
