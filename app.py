import telebot
import yt_dlp
import os

TOKEN = "8357499732:AAFYRlqZbINCxGtgcaBCvS-d6jSb_5QRkf0"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "👋 Music Downloader Bot ပါဗျာ။ YouTube Link ပို့ပေးပါ။")

@bot.message_handler(func=lambda message: True)
def download(message):
    if "http" in message.text:
        msg = bot.reply_to(message, "⏳ သီချင်းပြောင်းနေပါပြီ...")
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '192'}],
            'outtmpl': '%(id)s.%(ext)s',
            'quiet': True,
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(message.text, download=True)
                filename = ydl.prepare_filename(info).replace(".webm", ".mp3").replace(".m4a", ".mp3")
            with open(filename, 'rb') as audio:
                bot.send_audio(message.chat.id, audio)
            os.remove(filename)
        except Exception as e:
            bot.reply_to(message, f"❌ Error: {str(e)}")

if __name__ == "__main__":
    bot.infinity_polling()
