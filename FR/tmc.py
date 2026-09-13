#! /usr/bin/python3

import requests
import json
import re

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'

# API isteğini çalışan L_LCI üzerinden yap
s = requests.Session()
resplink = s.get('https://mediainfo.tf1.fr/mediainfocombo/L_LCI?context=ONEINFO&format=hls', headers={'User-Agent': USER_AGENT})

try:
    response_json = json.loads(resplink.text)
    mastlnk = response_json["delivery"]["url"]
except (KeyError, json.JSONDecodeError):
    print("API'den beklenen JSON yapısı alınamadı. Gelen yanıt:")
    print(resplink.text)
    exit(1)

# TMC tabanlı base_url hazırlığı (çıktı ve satır dönüştürmeleri için)
first_tmc_cdn = mastlnk.replace("alive-lci-hls", "alive-tmc-hls")
second_get_tmc = first_tmc_cdn.replace("prod/LCI/cmaf/out/LCI.m3u8", "prod/TMC/cmaf/out/TMC.m3u8")
base_url = second_get_tmc.replace("/TMC.m3u8", "/")

# Raw tmcfr.txt şablonunu çağır
try:
    tmc_res = s.get('https://raw.githubusercontent.com/bnyusuf15-alt/francetv-index/refs/heads/main/templates/tmcfr.txt', headers={'User-Agent': USER_AGENT})
    tmc_res.raise_for_status()
    m3u8_content = tmc_res.text
except Exception:
    print("tmcfr.txt şablonu alınamadı.")
    exit(1)

if m3u8_content and "#EXTM3U" in m3u8_content:
    lines = [line.strip() for line in m3u8_content.splitlines() if line.strip()]
    
    version_line = "#EXT-X-VERSION:3" # Varsayılan
    independent_tag = "#EXT-X-INDEPENDENT-SEGMENTS"
    body_lines = []
    
    for line in lines:
        if line.startswith("#EXT-X-VERSION:"):
            version_line = line
        elif line == "#EXT-X-INDEPENDENT-SEGMENTS":
            continue
        elif line.startswith("#EXTM3U"):
            continue
        else:
            # LCI içeriğindeki tüm URL ve yolları TMC'ye çevir ve base_url ekle
            line = line.replace('alive-lci-hls', 'alive-tmc-hls').replace('prod/LCI', 'prod/TMC').replace('LCI.m3u8', 'TMC.m3u8').replace('LCI', 'TMC')
            
            if 'URI="' in line:
                def fix_uri(match):
                    uri_val = match.group(1).replace('LCI', 'TMC')
                    if not uri_val.startswith('http'):
                        return f'URI="{base_url + uri_val}"'
                    return f'URI="{uri_val}"'
                line = re.sub(r'URI="([^"]+)"', fix_uri, line)
            
            if not line.startswith('#') and not line.startswith('http'):
                line = base_url + line
            elif not line.startswith('#') and line.startswith('http'):
                line = line.replace('LCI', 'TMC')
                
            body_lines.append(line)

    # Standart sıralama ile çıktıyı bas
    print('#EXTM3U')
    print(version_line)
    print(independent_tag)
    
    for line in body_lines:
        print(line)
else:
    print('#EXTM3U')
    print('#EXT-X-VERSION:6')
    print('#EXT-X-INDEPENDENT-SEGMENTS')
    print(base_url)
    new3_string = second_get_tmc.replace("/TMC.m3u8", "/TMC-mp4a_140800_fra=20000.m3u8")
    print('#EXT-X-MEDIA:TYPE=AUDIO,GROUP-ID="audio-AACL-141",CHANNELS="2",LANGUAGE="fr",NAME="Français",DEFAULT=YES,AUTOSELECT=YES,URI="{}"'.format(new3_string))
