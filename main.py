import os
import threading
import time
from telegram import Update
from telegram.ext import Updater, CommandHandler
from web3 import Web3
from config import TELEGRAM_BOT_TOKEN, ADMIN_CHAT_ID, HYPERLIQUID_RPC_URL, EXAMPLE_TRADER

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
                'stop_loss': 28000,
                'take_profit': 29500,
                'direction': 'long' if int(time.time()) % 2 == 0 else 'short',
                'size': 1500,
                'nickname': 'Sample-Trader'
            }
            time.sleep(30)

class TelegramBot:
    def __init__(self, token):
        self.updater = Updater(token=token)
        self.updater.dispatcher.add_handler(CommandHandler('start', self.start))
        
    def start(self, update: Update, context):
        update.message.reply_text('🤖 Hyperliquid Trade Bot Active!')

    def send_alert(self, chat_id, trade_info):
        msg = f"🚨 New Trade\n📊 Size: ${trade_info['size']:,.2f}\n💰 Price: {trade_info['entry_price']}"
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