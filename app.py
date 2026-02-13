import os
import telebot
import yt_dlp
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

# ၁။ လူကြီးမင်း ပေးထားသော Bot Token
BOT_TOKEN = '8357499732:AAFYRlqZbINCxGtgcaBCvS-d6jSb_5QRkf0'
bot = telebot.TeleBot(BOT_TOKEN)

# ၂။ Koyeb Health Check အတွက် Port 8000 ဖွင့်ခြင်း
def run_health_server():
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")
    
    server = HTTPServer(('0.0.0.0', 8000), Handler)
    server.serve_forever()

# ၃။ Bot ရဲ့ အလုပ်လုပ်ပုံ (YouTube & TikTok Support)
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "👋 Music Downloader Bot မှ ကြိုဆိုပါတယ်ဗျာ။\n\n🎵 YouTube သို့မဟုတ် TikTok Link ပို့ပေးပါ။ သီချင်းအဖြစ် ပြောင်းပေးပါ့မယ်။")

@bot.message_handler(func=lambda message: True)
def download_music(message):
    url = message.text
    if "youtube.com" in url or "youtu.be" in url or "tiktok.com" in url:
        msg = bot.reply_to(message, "⏳ သီချင်းပြောင်းနေပါပြီ၊ ခဏစောင့်ပေးပါ...")
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'ffmpeg_location': '/usr/bin/ffmpeg', 
            'outtmpl': '%(title)s.%(ext)s',
            'quiet': True,
            'no_warnings': True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info).replace('.webm', '.mp3').replace('.m4a', '.mp3')
                
                with open(filename, 'rb') as audio:
                    bot.send_audio(message.chat.id, audio)
                
                if os.path.exists(filename):
                    os.remove(filename)
                    
            bot.delete_message(message.chat.id, msg.message_id)

        except Exception as e:
            bot.edit_message_text(f"❌ Error: {str(e)}", message.chat.id, msg.message_id)
    else:
        bot.reply_to(message, "⚠️ ကျေးဇူးပြု၍ မှန်ကန်သော YouTube သို့မဟုတ် TikTok Link ကို ပို့ပေးပါ။")

# ၄။ Bot ကို စတင်မောင်းနှင်ခြင်း
if __name__ == "__main__":
    # Health server ကို Background မှာ မောင်းမယ်
    threading.Thread(target=run_health_server, daemon=True).start()
    print("Bot is running...")
    bot.infinity_polling()
