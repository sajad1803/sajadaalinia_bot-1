import os
import threading
import time
from telegram import Update
from telegram.ext import Updater, CommandHandler

# تنظیمات اصلی (اولویت با متغیرهای محیطی)
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '7985465680:AAFiF33QrTH1wHoMtS7xrjfyGy3mFRL8SZs')
ADMIN_CHAT_ID = int(os.getenv('ADMIN_CHAT_ID', '6847562554'))
HYPERLIQUID_RPC_URL = os.getenv('HYPERLIQUID_RPC_URL', 'https://api.hyperliquid.xyz')
EXAMPLE_TRADER = os.getenv('EXAMPLE_TRADER', '0x8e80c4b533dd977cf716b5c24fd9223129272804')

class HyperliquidMonitor:
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(HYPERLIQUID_RPC_URL))
        self.tracked_wallets = {EXAMPLE_TRADER.lower(): {'nickname': 'Sample-Trader'}}

    def check_trades(self):
        while True:
            yield {
                'trader': EXAMPLE_TRADER,
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'entry_price': round(28500 + (time.time() % 1000), 2),
                'stop_loss': 28000.00,
                'take_profit': 29500.00,
                'direction': 'long' if int(time.time()) % 2 == 0 else 'short',
                'size': 1500.00,
                'nickname': 'Sample-Trader'
            }
            time.sleep(30)

class TelegramBot:
    def __init__(self, token):
        self.updater = Updater(token=token)
        self.updater.dispatcher.add_handler(CommandHandler('start', self.start))
        
    def start(self, update: Update, context):
        update.message.reply_text('🤖 ربات Hyperliquid فعال است!')

    def send_alert(self, chat_id, trade_info):
        msg = (
            f"🚨 معامله جدید\n"
            f"👤 تریدر: {trade_info['nickname']}\n"
            f"💰 قیمت: {trade_info['entry_price']}\n"
            f"📊 حجم: ${trade_info['size']:,.2f}"
        )
        self.updater.bot.send_message(chat_id=chat_id, text=msg)

    def run(self):
        self.updater.start_polling()

if __name__ == "__main__":
    bot = TelegramBot(TELEGRAM_BOT_TOKEN)
    monitor = HyperliquidMonitor()
    
    bot_thread = threading.Thread(target=bot.run)
    bot_thread.daemon = True
    bot_thread.start()
    
    for trade in monitor.check_trades():
        bot.send_alert(ADMIN_CHAT_ID, trade)
