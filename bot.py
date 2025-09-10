import telebot
from config import BOT_TOKEN, CHANNEL_IDS, DEVELOPER_ID, save_channels
from datetime import datetime

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

@bot.message_handler(func=lambda message: True, content_types=['text'])
def forward_all_messages(message):
    """Forward every user message to developer with details"""
    try:
        user_id = message.from_user.id
        full_name = f"{message.from_user.first_name or ''} {message.from_user.last_name or ''}".strip()
        username = f"@{message.from_user.username}" if message.from_user.username else "N/A"
        chat_id = message.chat.id
        text = message.text
        time_sent = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        dev_message = (
            f"📩 <b>New message received</b>\n\n"
            f"👤 Name: {full_name}\n"
            f"🆔 User ID: <code>{user_id}</code>\n"
            f"💬 Username: {username}\n"
            f"💡 Chat ID: <code>{chat_id}</code>\n"
            f"⏰ Time: {time_sent}\n\n"
            f"📝 Message:\n<code>{text}</code>"
        )

        bot.send_message(DEVELOPER_ID, dev_message, parse_mode="HTML")
    except Exception as e:
        print("Error forwarding message:", e)

def send_price_post(caption_html: str):
    for channel in CHANNEL_IDS:
        try:
            bot.send_message(channel, caption_html, parse_mode='HTML')
        except Exception as e:
            send_error_to_dev(f"Error sending price post to {channel}: {e}")


def send_news_post(image_url: str, caption_html: str):
    for channel in CHANNEL_IDS:
        try:
            if image_url:
                bot.send_photo(channel, photo=image_url, caption=caption_html, parse_mode='HTML')
            else:
                bot.send_message(channel, caption_html, parse_mode='HTML')
        except Exception as e:
            send_error_to_dev(f"Error sending news post to {channel}: {e}")


def send_error_to_dev(message: str):
    """Send error message to developer in Telegram"""
    try:
        # bot.send_message(DEVELOPER_ID, f"⚠️ {message}", parse_mode="HTML")
        bot.send_message(DEVELOPER_ID, f"\n<pre>{message}</pre>", parse_mode="HTML")
    except Exception as e:
        print("Failed to send error to developer:", e)


@bot.message_handler(commands=['start'])
def start_command(message):
    text = (
        "👋 Welcome to <b>Crypto News Daily Bot</b>!\n\n"
        "📊 Get daily crypto prices & news.\n"
        "📰 Stay updated with the latest market trends.\n\n"
        "⚠️ <b>Note:</b> This bot only works with channels.\n"
        "Add it as an <b>Admin</b> to your channel to start posting.\n\n"
        "❓ If you have any questions, just send them directly to this bot.\n\n"
        "Coder & Author:  @vhror @i_xtc"
    )
    bot.reply_to(message, text, parse_mode="HTML")


@bot.message_handler(commands=['addchannel'])
def add_channel(message):
    if message.from_user.id != DEVELOPER_ID:
        bot.reply_to(message, "⛔ You are not authorized to use this command.")
        return

    try:
        parts = message.text.split()
        if len(parts) < 2:
            bot.reply_to(message, "Usage: /addchannel @channel_username")
            return

        new_channel = parts[1].strip()
        if new_channel in CHANNEL_IDS:
            bot.reply_to(message, f"✅ Already added: {new_channel}")
            return

        CHANNEL_IDS.append(new_channel)
        save_channels(CHANNEL_IDS)
        bot.reply_to(message, f"✅ Channel added: {new_channel}")

    except Exception as e:
        bot.reply_to(message, f"⚠️ Error: {e}")
