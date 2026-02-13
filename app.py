import os
import telebot
import yt_dlp

# လူကြီးမင်းရဲ့ Bot Token ကို ဒီမှာ ထည့်ပါ
BOT_TOKEN = '8357499732:AAFYRlqZbINCxGtgcaBCvS-d6jSb_5QRkf0'
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    # YouTube ကော TikTok ပါ ရကြောင်း စာသား ပြောင်းလဲထားပါတယ်
    bot.reply_to(message, "👋 Music Downloader Bot မှ ကြိုဆိုပါတယ်ဗျာ။\n\n🎵 YouTube Link (သို့မဟုတ်) TikTok Link ကို ပို့ပေးပါ။ ကျွန်တော် သီချင်းအဖြစ် ပြောင်းပေးပါ့မယ်။")

@bot.message_handler(func=lambda message: True)
def download_music(message):
    url = message.text
    if "youtube.com" in url or "youtu.be" in url or "tiktok.com" in url:
        msg = bot.reply_to(message, "⏳ သီချင်းပြောင်းနေပါပြီ၊ ခဏစောင့်ပေးပါ...")
        
        # Error မတက်အောင် FFmpeg location ကို အသေ သတ်မှတ်ထားပါတယ်
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'ffmpeg_location': '/usr/bin/ffmpeg', # Koyeb/Linux FFmpeg path
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
                
                # ပို့ပြီးရင် ဖိုင်ကို ပြန်ဖျက်မယ် (Storage မပြည့်အောင်)
                if os.path.exists(filename):
                    os.remove(filename)
                    
            bot.delete_message(message.chat.id, msg.message_id)

        except Exception as e:
            bot.edit_message_text(f"❌ Error တက်သွားပါတယ်ဗျာ- {str(e)}", message.chat.id, msg.message_id)
    else:
        bot.reply_to(message, "⚠️ ကျေးဇူးပြု၍ မှန်ကန်သော YouTube သို့မဟုတ် TikTok Link ကို ပို့ပေးပါ။")

if __name__ == "__main__":
    print("Bot is running...")
    bot.infinity_polling()
