import os
import threading
import time
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from web3 import Web3

# تنظیمات اصلی
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN', '7985465680:AAFiF33QrTH1wHoMtS7xrjfyGy3mFRL8SZs')
ADMIN_CHAT_ID = int(os.getenv('ADMIN_CHAT_ID', '6847562554'))
HYPERLIQUID_RPC = os.getenv('HYPERLIQUID_RPC', 'https://api.hyperliquid.xyz')
EXAMPLE_WALLET = os.getenv('EXAMPLE_WALLET', '0x8e80c4b533dd977cf716b5c24fd9223129272804')

class TradeMonitor:
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(HYPERLIQUID_RPC))
        self.tracked_wallets = {EXAMPLE_WALLET.lower(): {'nickname': 'Trader-1'}}

    def check_trades(self):
        """شبیه‌ساز جریان معاملات"""
        while True:
            yield {
                'trader': EXAMPLE_WALLET,
                'time': time.strftime('%Y-%m-%d %H:%M:%S'),
                'price': round(28500 + (time.time() % 1000), 2),
                'direction': 'LONG' if int(time.time()) % 2 == 0 else 'SHORT',
                'size': 1500.00
            }
            time.sleep(30)

class TelegramBot:
    def __init__(self):
        self.updater = Updater(TELEGRAM_TOKEN)
        self.setup_handlers()

    def setup_handlers(self):
        self.updater.dispatcher.add_handler(CommandHandler('start', self.start))

    def start(self, update: Update, context: CallbackContext):
        update.message.reply_text('🤖 ربات ردیابی هایپرلیکویید فعال شد!')

    def send_alert(self, trade):
        message = (
            f"🔔 معامله جدید\n"
            f"🆔 {trade['trader'][:6]}...{trade['trader'][-4:]}\n"
            f"📊 حجم: ${trade['size']:,.2f}\n"
            f"💰 قیمت: {trade['price']}\n"
            f"📌 جهت: {trade['direction']}\n"
            f"⏰ زمان: {trade['time']}"
        )
        self.updater.bot.send_message(chat_id=ADMIN_CHAT_ID, text=message)

    def run(self):
        self.updater.start_polling()

if __name__ == "__main__":
    print("🚀 در حال راه‌اندازی ربات...")
    
    bot = TelegramBot()
    monitor = TradeMonitor()
    
    # راه‌اندازی ربات در ترد جداگانه
    bot_thread = threading.Thread(target=bot.run)
    bot_thread.daemon = True
    bot_thread.start()
    
    # شروع ردیابی معاملات
    for trade in monitor.check_trades():
        bot.send_alert(trade)
