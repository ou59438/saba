import discord
import whisper
import asyncio
from discord.ext import commands
from discord import FFmpegPCMAudio
import os

# Whisper modelini yükle
model = whisper.load_model("base")  # "base", "small", "medium", "large" seçenekleri

# Discord botunu oluştur
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Sesli kanal dinleme ve konuşmaları metne dökme
@bot.command()
async def listen(ctx):
    # Sesli kanal varsa bağlan
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        vc = await channel.connect()

        # Ses kaydını başlat
        # FFmpeg ile sesli kanalın sesini kaydetmek için burada uygun bir yöntem ekleyin
        ffmpeg_options = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
        }

        # FFmpeg ile sesli kanaldan ses almak
        audio_source = FFmpegPCMAudio("input_audio.wav", **ffmpeg_options)

        # Ses kaydını bir dosyaya yaz
        with open("audio.wav", "wb") as f:
            f.write(audio_source)

        # Ses dosyasını Whisper ile metne dönüştür
        result = model.transcribe("audio.wav")

        # Sonucu Discord kanalına yazdır
        await ctx.send(f"Transcription: {result['text']}")

        # Sesli kanaldan çık
        await vc.disconnect()

# Botu çalıştır
bot.run('MTMxMDIyNzYwNTQyNDgzNjY5MA.Gk1rIL.0___qHIRL1XF6TsYQZVLJf4u3XOHUsOtPebyfg')