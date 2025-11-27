BlueFireFamily | AI Bot
===========================
Güncel tarih: 27.11.2025

Bu paket, BlueFireFamily topluluğu için hazırlanmış ücretsiz altyapılarla uyumlu,
gelişmiş yapay zeka destekli bir Discord botu örneğidir.

Bot Adı: **BlueFireFamily | AI Bot**
Dosya içeriği:
  - main.py
  - requirements.txt
  - .env (sizin oluşturmanız gerekiyor, .env.example içerikte)
  - README_BFF_AI_Bot_TR.txt (bu dosya)

----------------------------------------
1. GENEL ÖZELLİKLER
----------------------------------------
- Slash komut destekli (Discord'un yeni komut sistemi)
- /ai ile yapay zeka sohbeti
- /imagine ile görsel üretim prompt taslağı
- /ping ve /yardim komutları
- Kullanıcı başına kısa süreli hafıza (son 5 mesaj)
- Tek kodla birden fazla OpenAI uyumlu sağlayıcıyı kullanabilme:
  * OpenAI
  * Groq (openai uyumlu endpoint)
  * DeepSeek
  * Together
  * OpenRouter
  * ve diğer OpenAI-uyumlu API sağlayıcıları

Not: Tamamen ücretsiz ve %100 kesintisiz 7/24 çalışan altyapı pratikte çok zordur.
Çoğu ücretsiz hosting hizmeti belirli süre sonra projeyi uyku moduna alır.
Ancak aşağıdaki çözümlerle uzun süre kesintisiz çalışmaya çok yaklaşabilirsiniz.

----------------------------------------
2. ÜCRETSİZ / DÜŞÜK MALİYETLİ ALTYAPI ÖNERİLERİ
----------------------------------------

A) Yapay Zeka Servisleri (OpenAI Uyumlu)
----------------------------------------
1) OpenAI
   - Genelde yeni hesaplara küçük bir deneme bakiyesi verilir (değişebilir).
   - Resmi ve stabil altyapı.
   - API URL: https://api.openai.com/v1
   - Örnek model: gpt-4o-mini

2) Groq
   - LLaMA tabanlı güçlü modeller sunar, OpenAI uyumlu endpoint sağlar.
   - API URL: https://api.groq.com/openai/v1
   - Örnek model: llama-3.3-70b-versatile

3) DeepSeek
   - Uygun fiyatlı / ücretsiz kota sunabilen bir sağlayıcıdır.
   - API URL (örnek): https://api.deepseek.com/v1

4) Together, OpenRouter vb.
   - Birçok model sağlayan platformlar, çoğunlukla OpenAI uyumlu endpoint sunarlar.
   - Sadece base URL ve model adını değiştirerek bu botla kullanılabilirler.

B) Hosting / Çalıştırma Altyapıları
----------------------------------------
1) Kendi Bilgisayarın (Tamamen Ücretsiz, ama PC açık kalmalı)
   - Avantaj: Ücret yok, kontrol sende.
   - Dezavantaj: PC kapalıyken bot da kapanır.

2) Ücretsiz / Düşük Maliyetli Cloud Platformlar
   - Railway, Render, Deta, Fly.io gibi servisler zaman zaman ücretsiz tier sunar.
   - Ücretsiz katmanlarda:
     * CPU süresi kısıtlı olabilir
     * Inaktif olduğunda uyku moduna geçebilir
   - Hafif botlar için uzun süre 7/24'e yakın çalışabilir.

3) Düşük Ücretli VPS (Gerçek 7/24 için en sağlıklısı)
   - 4–5 USD/ay civarı ucuz VPS'ler var.
   - Tam 7/24 ve sınırlama olmadan botu çalıştırabilirsiniz.

----------------------------------------
3. GEREKEN HESAPLAR
----------------------------------------
1) Discord developer hesabı (Discord hesabın zaten varsa hazır demektir)
2) En az bir yapay zeka sağlayıcısında API anahtarı
   - Örnek: OpenAI, Groq, DeepSeek, Together, OpenRouter vb.

----------------------------------------
4. DISCORD BOT OLUŞTURMA ADIMLARI
----------------------------------------
1) https://discord.com/developers/applications adresine git.
2) Sağ üstten "New Application" butonuna tıkla.
3) Uygulama adına "BlueFireFamily | AI Bot" yaz ve oluştur.
4) Sol menüden **Bot** sekmesine git:
   - "Add Bot" butonuna tıkla, onayla.
   - "Reset Token" veya "Copy Token" ile bot token'ını kopyala.
   - Bu token'i `.env` dosyasında `DISCORD_TOKEN=` satırına yapıştıracaksın.
5) "Privileged Gateway Intents" bölümünde:
   - **MESSAGE CONTENT INTENT** seçeneğini aktif et (botun mesaj içeriklerini görebilmesi için).
6) Sol menüden **OAuth2 > URL Generator** bölümüne git:
   - Scopes kısmında **bot** ve **applications.commands** seç.
   - Bot Permissions kısmında en azından:
     * Send Messages
     * Read Message History
     * Use Slash Commands
   - Oluşan URL'yi kopyalayıp tarayıcıda aç ve botu sunucuna ekle.

----------------------------------------
5. PROJE KURULUM ADIMLARI (YEREL PC)
----------------------------------------

A) Python Kurulumu
-------------------
1) https://python.org üzerinden en az Python 3.10+ sürümünü indir.
2) Kurarken "Add Python to PATH" kutucuğunu işaretlemeyi unutma.

B) Klasör ve Dosya Yapısı
--------------------------
1) Bir klasör oluştur:
   Örneğin: C:\projeler\bff_ai_bot
2) Bu zip içindeki dosyaları bu klasöre çıkart:
   - main.py
   - requirements.txt
   - README_BFF_AI_Bot_TR.txt

C) Sanal Ortam (Opsiyonel ama tavsiye edilir)
---------------------------------------------
Komut satırında (CMD / PowerShell) klasöre gir:

    cd C:\projeler\bff_ai_bot

Sanal ortam oluştur:

    python -m venv venv

Aktifleştir:

- Windows (CMD):

    venv\Scripts\activate

- PowerShell:

    venv\Scripts\Activate.ps1

Aktif olduğunda başta `(venv)` yazar.

D) Gerekli Kütüphanelerin Kurulumu
----------------------------------

    pip install -r requirements.txt

E) .env Dosyası Oluşturma
--------------------------
1) Aynı klasörde `.env` adında yeni bir dosya oluştur.
2) Aşağıdaki örneği içerisine yapıştır ve kendine göre düzenle:

----------------------------------------
ÖRNEK .env İÇERİĞİ
----------------------------------------
# BlueFireFamily | AI Bot - Örnek .env Dosyası

# ZORUNLU: Discord bot tokeniniz
DISCORD_TOKEN=BURAYA_DISCORD_BOT_TOKENINIZI_YAZIN

# YAPAY ZEKA SAĞLAYICI AYARLARI
# Sadece log/listeleme amaçlı etiket
AI_PROVIDER_NAME=openai

# ZORUNLU: Seçtiğiniz sağlayıcıya ait API anahtarınız
AI_API_KEY=BURAYA_AI_API_KEYINIZI_YAZIN

# OpenAI uyumlu API taban adresi
# Örnekler:
#   OpenAI   : https://api.openai.com/v1
#   Groq     : https://api.groq.com/openai/v1
#   DeepSeek : https://api.deepseek.com/v1
#   Together : https://api.together.xyz/v1
#   OpenRouter: https://openrouter.ai/api/v1
AI_BASE_URL=https://api.openai.com/v1

# Model adı (seçtiğiniz servise göre değişir)
# Örnekler:
#   OpenAI: gpt-4o-mini, gpt-4.1-mini, gpt-4.1
#   Groq  : llama-3.3-70b-versatile (örnek)
#   DeepSeek: deepseek-chat vb.
AI_MODEL=gpt-4o-mini

# İsteğe bağlı ayarlar
AI_MAX_TOKENS=512
AI_TEMPERATURE=0.7

----------------------------------------

----------------------------------------
6. BOTU ÇALIŞTIRMA
----------------------------------------

Sanal ortam aktifken:

    python main.py

Konsolda:

    [INFO] BlueFireFamily | AI Bot başlatılıyor...
    [INFO] Bot giriş yaptı: BlueFireFamily | AI Bot#1234 (ID: ...)

gibi loglar görmelisin.

Discord'da botunun çevrimiçi (online) olduğunu görüyorsan,
her şey yolunda demektir.

Denemek için sunucunda:

  - /yardim
  - /ai Merhaba, nasılsın?
  - /imagine mavi alevli gamer logo

komutlarını kullanabilirsin.

----------------------------------------
7. 7/24 ÇALIŞTIRMA İÇİN ÖNERİLER
----------------------------------------

A) Kendi PC'n Üzerinde
----------------------
- Bilgisayarını kapatmadığın, uyku moduna almadığın sürece bot 7/24 çalışır.
- Windows'ta botu otomatik başlatmak için:
  * Görev Zamanlayıcı (Task Scheduler) ile oturum açınca script başlatılabilir.

B) Ücretsiz Cloud (Railway / Render vb.)
----------------------------------------
Genel mantık:
1) GitHub repo oluştur, bu projeyi oraya yükle.
2) Railway veya Render hesabı aç (GitHub ile giriş yapılabiliyor).
3) Yeni bir "Web Service" / "App" oluşturup GitHub repo'nu bağla.
4) Ortam değişkenleri (Environment Variables) kısmına `.env` içeriğindeki
   değişkenleri tek tek tanımla (DISCORD_TOKEN, AI_API_KEY vb.).
5) Build ve run komutlarını şu şekilde ayarla:
   - Build: `pip install -r requirements.txt`
   - Run: `python main.py`
6) Deploy et. Proje ayağa kalkınca bot çalışmaya başlar.

Not: Ücretsiz planlarda belirli saat sonra inaktif kalırsa uykuya geçebilir.
Yine de çoğu zaman uzun süre kesintisiz çalışacaktır.

C) VPS Üzerinde Systemd Servisi (Linux)
----------------------------------------
1) Projeyi VPS'e kopyala (scp / git clone).
2) Gerekli Python ortamını kur, `pip install -r requirements.txt` çalıştır.
3) `/etc/systemd/system/bff_ai_bot.service` dosyası oluştur:

    [Unit]
    Description=BlueFireFamily AI Discord Bot
    After=network.target

    [Service]
    Type=simple
    WorkingDirectory=/home/kullanici/bff_ai_bot
    ExecStart=/home/kullanici/bff_ai_bot/venv/bin/python main.py
    Restart=always

    [Install]
    WantedBy=multi-user.target

4) Komutlar:

    sudo systemctl daemon-reload
    sudo systemctl enable bff_ai_bot
    sudo systemctl start bff_ai_bot

Böylece VPS yeniden başlasa bile bot otomatik çalışır.

----------------------------------------
8. SIK KARŞILAŞILAN HATALAR
----------------------------------------

1) HATA: "HATA: .env içinde DISCORD_TOKEN tanımlı değil!"
   - Çözüm: `.env` dosyasını oluşturup DISCORD_TOKEN satırını doldur.

2) Slash komutlar görünmüyor
   - İlk çalıştırmadan sonra Discord tarafında slash komutlarının
     çıkması 1–5 dakika sürebilir.
   - Botu yeniden başlatmana gerek yok, biraz bekle.

3) AI servisi hata veriyor
   - Konsol loguna bak:
     * 401 -> API key yanlış veya yetkisiz
     * 404 -> Yanlış endpoint (AI_BASE_URL yanlış olabilir)
     * 429 -> Kota aşıldı (rate limit / quota)
   - Sağlayıcının panelinden:
     * Model adını (AI_MODEL)
     * Base URL'yi (AI_BASE_URL)
     * API key'i (AI_API_KEY)
     güncellediğinden emin ol.

----------------------------------------
9. TASARIM NOTLARI
----------------------------------------
- Botun durum mesajında "BlueFireFamily | AI Assistant" yazar.
- Embed başlıklarında BlueFireFamily ismi ve oyun/sohbet kimliğine uygun
  ikonlar kullanılmıştır.
- İstersen:
  * Renkleri değiştir (discord.Color.blurple() vs.)
  * /ai komutunun sadece belirli kanal/kategori'de çalışmasını sağlayabilirsin.

----------------------------------------
10. GELİŞTİRMEYE DEVAM ETMEK İÇİN İPUÇLARI
----------------------------------------
- Kullanıcıya özel komutlar ekle (örn: /profil, /istatistik, /sunucu).
- AI yanıtlarını log dosyasına da yazdırarak istatistik toplayabilirsin.
- Belirli rollere özel premium AI modelleri kullandırma gibi sistemler
  ekleyebilirsin.

Herhangi bir yerde takılırsan, elindeki hata mesajları ve .env içeriğini
(anahtarları gizleyerek) bana gönderirsen, birlikte debug edebiliriz. :)
