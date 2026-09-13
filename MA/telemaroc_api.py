from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests
import re
import json

# Bot korumalarını aşmak için User-Agent header'ı
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# Step 1: HTML sayfasını güvenli şekilde çek
html_url = "https://www.telemaroc.tv/liveTV"
response = requests.get(html_url, headers=HEADERS)
response.raise_for_status()

# Step 2: BeautifulSoup ile iframe'i ve token/st/key gibi parametreleri esnek şekilde bul
soup = BeautifulSoup(response.text, "html.parser")
iframe = soup.find("iframe", src=re.compile(r"player\.restream\.io|player"))

if not iframe or not iframe.get("src"):
    raise ValueError("Oynatıcı iframe'i HTML içinde bulunamadı.")

iframe_src = iframe["src"]

# Parametre adı 'token', 'st', 'key' veya 'auth' olsa bile yakala
token_match = re.search(r'[?&](?:token|st|key|auth)=([\w-]+)', iframe_src)
if not token_match:
    # URL içerisindeki olası uzun token/hash dizilimini yakalamaya çalış
    token_match = re.search(r'/([a-f0-9]{16,}|[A-Za-z0-9_-]{20,})', iframe_src)

# Eğer iframe içinde bulunamadıysa, tüm sayfa kaynağında (response.text) ara
if not token_match:
    token_match = re.search(r'(?:token|st|key|auth)=([a-f0-9]{16,}|[A-Za-z0-9_-]{20,})', response.text)

if not token_match:
    token_match = re.search(r'/([a-f0-9]{16,}|[A-Za-z0-9_-]{20,})', response.text)
    
if not token_match:
    raise ValueError("İframe veya HTML içinde geçerli bir token/parametre bulunamadı.")

token = token_match.group(1)

# Step 3 & 4: Metadata'yı çek ve videoUrlHls'yi anahtar veya regex yedeklemesiyle bul
restream_metadata_url = f"https://player-backend.restream.io/public/videos/{token}?instant=true"
meta_response = requests.get(restream_metadata_url, headers=HEADERS)
meta_response.raise_for_status()

metadata = {}
try:
    metadata = meta_response.json()
except ValueError:
    pass

video_url_hls = metadata.get("videoUrlHls")
video_url_dash = metadata.get("videoUrlDash")
viewers_url = metadata.get("viewersUrl")

# API key adı değişirse veya bulunamazsa regex ile m3u8 uzantılı URL'yi yakala
if not video_url_hls:
    m3u8_matches = re.findall(r'https?://[^\s<>"]+?\.m3u8', meta_response.text)
    if m3u8_matches:
        video_url_hls = m3u8_matches[0]

if not video_url_hls:
    raise ValueError("Ne videoUrlHls anahtarı ne de regex ile m3u8 URL'si bulunamadı.")

# API key adı değişirse veya bulunamazsa regex ile m3u8 uzantılı URL'yi yakala
if not video_url_dash:
    mpd_matches = re.findall(r'https?://[^\s<>"]+?\.mpd', meta_response.text)
    if mpd_matches:
        video_url_dash = mpd_matches[0]

if not video_url_dash:
    raise ValueError("Ne anahtar ne de regex ile mpd URL'si bulunamadı.")

# API key adı değişirse veya bulunamazsa regex ile m3u8 uzantılı URL'yi yakala
if not viewers_url:
    viewer_matches = re.findall(r'https?://[^\s<>"]+?\views', meta_response.text)
    if viewer_matches:
        viewers_url = viewer_matches[0]

if not viewers_url:
    raise ValueError("Ne anahtar ne de regex ile izlenme URL'si bulunamadı.")
  
# Step 5 & 6: JSON Verisini kaydet
output_data = {
    "videoUrlDash": video_url_dash,
    "videoUrlHls": video_url_hls,
    "viewersUrl": viewers_url,
    "disableBrandingAvailable": True
}

print(json.dumps(output_data))
