#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BlueFireFamily | AI Bot
Gelişmiş yapay zeka destekli Discord botu.
Özellikler:
- /ai komutu ile yapay zeka sohbeti
- /imagine komutu ile prompt yazısını görsel promptuna dönüştürme (metin üretir, görsel API'sine gönderebilirsiniz)
- /ping ve /yardim komutları
- Kullanıcı başına kısa süreli hafıza (son 5 mesaj)
- Birden fazla OpenAI-uyumlu sağlayıcı ile çalışabilecek esnek yapı
"""

import os
import logging
import asyncio
import time
from typing import Dict, List, Optional

import discord
from discord import app_commands
from discord.ext import commands

import requests
from dotenv import load_dotenv

# -------------------------------------------------
# LOG AYARLARI
# -------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("BFF_AI_BOT")

# -------------------------------------------------
# .env YÜKLE
# -------------------------------------------------
load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
AI_PROVIDER_NAME = os.getenv("AI_PROVIDER_NAME", "openai")  # Sadece etiket, log için.
AI_API_KEY = os.getenv("AI_API_KEY")
AI_BASE_URL = os.getenv("AI_BASE_URL", "https://api.openai.com/v1")
AI_MODEL = os.getenv("AI_MODEL", "gpt-4o-mini")  # Sağlayıcıya göre değiştirin
AI_MAX_TOKENS = int(os.getenv("AI_MAX_TOKENS", "512"))
AI_TEMPERATURE = float(os.getenv("AI_TEMPERATURE", "0.7"))

if not DISCORD_TOKEN:
    raise SystemExit("HATA: .env içinde DISCORD_TOKEN tanımlı değil!")

if not AI_API_KEY:
    logger.warning("UYARI: AI_API_KEY tanımlı değil. /ai komutu hata verecektir.")

# -------------------------------------------------
# DISCORD INTENTS
# -------------------------------------------------
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Bot komut prefix'i pek kullanmıyoruz, slash komut tercihli.
bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None
)

# Kullanıcı başına hafıza: {user_id: [ {role, content}, ... ]}
USER_MEMORY: Dict[int, List[Dict[str, str]]] = {}
MAX_MEMORY_MESSAGES = 5


# -------------------------------------------------
# AI İSTEK FONKSİYONLARI
# -------------------------------------------------
def build_headers() -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {AI_API_KEY}",
        "Content-Type": "application/json",
    }


def build_payload(messages: List[Dict[str, str]]) -> Dict:
    """
    OpenAI-chat uyumlu payload.
    Çoğu alternatif sağlayıcı (Groq, DeepSeek, OpenRouter, Together, xAI vb.)
    benzer yapıyı /chat/completions endpoint'i ile destekliyor.
    """
    return {
        "model": AI_MODEL,
        "messages": messages,
        "max_tokens": AI_MAX_TOKENS,
        "temperature": AI_TEMPERATURE,
    }


def call_ai_api(messages: List[Dict[str, str]]) -> str:
    if not AI_API_KEY:
        return "⚠️ Yapay zeka API anahtarı ayarlanmamış. Lütfen bot sahibine bildirin."

    url = AI_BASE_URL.rstrip("/") + "/chat/completions"
    headers = build_headers()
    payload = build_payload(messages)

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=60)
    except requests.RequestException as e:
        logger.error(f"AI isteği hata verdi: {e}")
        return "⚠️ Yapay zeka servisine ulaşılamadı. Birazdan tekrar deneyin."

    if resp.status_code != 200:
        logger.error(f"AI yanıt kodu {resp.status_code}: {resp.text[:500]}")
        return f"⚠️ Yapay zeka servisi hata döndürdü (kod: {resp.status_code})."

    try:
        data = resp.json()
    except Exception as e:
        logger.error(f"AI yanıt JSON hatası: {e} - Text: {resp.text[:500]}")
        return "⚠️ Yapay zeka yanıtı çözülemedi."

    # OpenAI uyumlu cevap
    try:
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        logger.error(f"AI yanıt parse hatası: {e} - JSON: {data}")
        return "⚠️ Yapay zeka yanıtı beklenen formatta değil."


def push_user_memory(user_id: int, role: str, content: str):
    """
    Kullanıcı hafızasına yeni bir mesaj ekler.
    Sadece kısa süreli, RAM üzerinde bir hafızadır. Bot yeniden başlarsa sıfırlanır.
    """
    if user_id not in USER_MEMORY:
        USER_MEMORY[user_id] = []

    USER_MEMORY[user_id].append({"role": role, "content": content})

    # Limit aşılırsa eskileri sil
    if len(USER_MEMORY[user_id]) > MAX_MEMORY_MESSAGES:
        USER_MEMORY[user_id] = USER_MEMORY[user_id][-MAX_MEMORY_MESSAGES:]


def build_user_conversation(user_id: int, user_prompt: str) -> List[Dict[str, str]]:
    """
    Kullanıcı geçmişi + sistem mesajı + son prompt'u birleştirir.
    """
    system = {
        "role": "system",
        "content": (
            "Sen BlueFireFamily topluluğuna özel, Türkçe konuşan bir yapay zeka asistansın. "
            "Kibar, açıklayıcı ve teknik konularda detaycı yanıtlar ver. "
            "Kısa ama anlaşılır mesajlar yaz; gerektiğinde maddeli anlat."
        ),
    }

    history = USER_MEMORY.get(user_id, []).copy()
    history.insert(0, system)
    history.append({"role": "user", "content": user_prompt})
    return history


# -------------------------------------------------
# OLAYLAR
# -------------------------------------------------
@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        logger.info(f"Slash komutları senkronize edildi ({len(synced)} komut).")
    except Exception as e:
        logger.error(f"Slash komut senkronizasyon hatası: {e}")

    logger.info(f"Bot giriş yaptı: {bot.user} (ID: {bot.user.id})")
    activity = discord.Game(name="BlueFireFamily | AI Assistant")
    await bot.change_presence(status=discord.Status.online, activity=activity)


# -------------------------------------------------
# YARDIMCI FONKSİYONLAR
# -------------------------------------------------
async def defer_if_needed(interaction: discord.Interaction):
    """
    Eğer cevap üretimi biraz sürebilecekse, interaction'ı 'thinking...' moduna alır.
    """
    if not interaction.response.is_done():
        await interaction.response.defer(thinking=True)


# -------------------------------------------------
# SLASH KOMUTLAR
# -------------------------------------------------
@bot.tree.command(name="ping", description="Botun gecikmesini gösterir.")
async def ping_command(interaction: discord.Interaction):
    start = time.time()
    await interaction.response.defer(thinking=True)
    end = time.time()
    latency_ms = (bot.latency * 1000)
    api_ms = (end - start) * 1000

    embed = discord.Embed(
        title="🏓 BlueFireFamily | AI Bot",
        description="Ping bilgileri",
        color=discord.Color.blue(),
    )
    embed.add_field(name="Discord Gateway", value=f"{latency_ms:.0f} ms")
    embed.add_field(name="Komut Gecikmesi", value=f"{api_ms:.0f} ms")
    embed.set_footer(text="BlueFireFamily • 2011'den beri oyun & sohbet topluluğu")

    await interaction.followup.send(embed=embed, ephemeral=True)


@bot.tree.command(name="yardim", description="BlueFireFamily | AI Bot komutlarını gösterir.")
async def yardim_command(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🤖 BlueFireFamily | AI Bot Yardım",
        description=(
            "BlueFireFamily topluluğu için geliştirilmiş yapay zeka destekli yardımcı bottur.\n\n"
            "**Komutlar:**\n"
            "• `/ai soru:` Yapay zeka ile sohbet / soru-cevap.\n"
            "• `/imagine metin:` Verdiğiniz promptu görsel üretim API'lerine uygun hale getirir.\n"
            "• `/ping` Botun gecikmesini gösterir.\n\n"
            "Bot, birden fazla OpenAI uyumlu sağlayıcı ile çalışacak şekilde tasarlanmıştır."
        ),
        color=discord.Color.blurple(),
    )
    embed.add_field(
        name="Desteklenen Yapay Zeka Altyapıları",
        value=(
            "OpenAI, Groq, DeepSeek, Together, OpenRouter vb. OpenAI uyumlu API'ler.\n"
            "Sadece `.env` içinde `AI_BASE_URL`, `AI_MODEL` ve `AI_API_KEY` ayarlarını güncellemeniz yeterlidir."
        ),
        inline=False,
    )
    embed.set_footer(text="BlueFireFamily | AI Bot • /ai komutunu deneyin!")

    await interaction.response.send_message(embed=embed, ephemeral=True)


@bot.tree.command(name="ai", description="Yapay zeka destekli sohbet / soru-cevap.")
@app_commands.describe(soru="Sormak istediğiniz soru veya konuşmak istediğiniz konu.")
async def ai_command(interaction: discord.Interaction, soru: str):
    await defer_if_needed(interaction)

    user_id = interaction.user.id
    logger.info(f"/ai komutu kullanan: {interaction.user} (ID: {user_id})")

    push_user_memory(user_id, "user", soru)
    messages = build_user_conversation(user_id, soru)
    answer = await asyncio.to_thread(call_ai_api, messages)
    push_user_memory(user_id, "assistant", answer)

    # Yanıt çok uzunsa thread açalım
    if len(answer) > 1500 and isinstance(interaction.channel, (discord.TextChannel, discord.Thread)):
        base_msg = answer[:1500]
        rest_msg = answer[1500:]

        msg = await interaction.followup.send(base_msg)
        thread = await msg.create_thread(name=f"BlueFireFamily | AI - {interaction.user.display_name}")
        # Kalanı parçalayarak gönder
        for chunk_start in range(0, len(rest_msg), 1900):
            chunk = rest_msg[chunk_start:chunk_start + 1900]
            await thread.send(chunk)
    else:
        # Normal yanıt
        if interaction.response.is_done():
            await interaction.followup.send(answer)
        else:
            await interaction.response.send_message(answer)


@bot.tree.command(name="imagine", description="Görsel üretim için prompt taslağı oluşturur.")
@app_commands.describe(metin="Görselde ne olsun? (ör: 'mavi alevli, neon gamer logo')")
async def imagine_command(interaction: discord.Interaction, metin: str):
    await defer_if_needed(interaction)

    prompt = (
        f"Yüksek kaliteli, detaylı, dijital sanat tarzında bir görsel üretmek için İngilizce bir prompt yaz. "
        f"Stil: neon, siberpunk, oyun temalı, BlueFireFamily markasına yakışır. "
        f"Kullanıcının isteği: {metin!r}. "
        f"Prompt sadece İngilizce olsun, kısa ama detaylı olsun."
    )

    messages = [
        {
            "role": "system",
            "content": "Sen bir görsel prompt tasarımcısın. Sadece İngilizce prompt döndür.",
        },
        {
            "role": "user",
            "content": prompt,
        },
    ]

    answer = await asyncio.to_thread(call_ai_api, messages)

    embed = discord.Embed(
        title="🎨 Imagine Prompt (BlueFireFamily)",
        description="Aşağıdaki metni bir görsel üretim API'sine (DALL·E, Stable Diffusion vb.) gönderebilirsiniz:",
        color=discord.Color.dark_blue(),
    )
    embed.add_field(name="Prompt", value=answer[:1024], inline=False)
    embed.set_footer(text="BlueFireFamily | AI Bot")

    await interaction.followup.send(embed=embed)


# -------------------------------------------------
# MAIN
# -------------------------------------------------
def main():
    logger.info("BlueFireFamily | AI Bot başlatılıyor...")
    bot.run(DISCORD_TOKEN)


if __name__ == "__main__":
    main()
