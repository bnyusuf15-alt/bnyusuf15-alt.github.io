import os
import re
import requests
import urllib3

# SSL sertifika doğrulama uyarılarını kapatır (verify=False için)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

embed_urls = [
    "https://snrt.player.easybroadcast.io/events/73_aloula_w1dqfwm",
    "https://snrt.player.easybroadcast.io/events/73_arryadia_k2tgcj0",
    "https://snrt.player.easybroadcast.io/events/73_arrabia_hthcj4p",
    "https://snrt.player.easybroadcast.io/events/73_almaghribia_83tz85q",
    "https://snrt.player.easybroadcast.io/events/73_assadissa_7b7u5n1",
    "https://snrt.player.easybroadcast.io/events/73_tamazight_tccybxt",
    "https://snrt.player.easybroadcast.io/events/73_laayoune_pgagr52"
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36",
    "Referer": "https://snrt.player.easybroadcast.io/"
}

for embed_url in embed_urls:
    try:
        match = re.search(r'/events/([^/]+)', embed_url)
        if not match:
            continue
        name = match.group(1)
        
        parts = name.split('_')
        file_name = parts[1] if len(parts) > 1 else name
        output_file = f"MA/{file_name}.m3u8"
        
        print(f"İşleniyor: {file_name}...")

        url = f"https://token.easybroadcast.io/all?url=https://cdn.live.easybroadcast.io/abr_corp/{name}/playlist_dvr.m3u8"
        response = requests.get(url, headers=headers, verify=False)

        if response.status_code == 200:
            api_text = response.text.strip()
            
            # API'den gelen parametre sırası değişebileceği için bağımsız regex ile ayıklıyoruz
            token_match = re.search(r'token=([\w\-]+)', api_text)
            expires_match = re.search(r'expires=(\d+)', api_text)
            path_match = re.search(r'token_path=([^&]+)', api_text)

            if token_match and expires_match and path_match:
                token = token_match.group(1)
                expires = expires_match.group(1)
                token_path = path_match.group(1)
                
                # İstediğiniz özel token parametre dizgesi
                custom_token_query = f"token={token}&expires={expires}&token_path={token_path}"
            else:
                custom_token_query = api_text

            hls_variant_link = f"https://cdn.live.easybroadcast.io/abr_corp/{name}/playlist_dvr.m3u8?{custom_token_query}"
            
            stream_response = requests.get(hls_variant_link, headers=headers, verify=False)
            stream_response.raise_for_status()

            base_url = f"https://cdn.live.easybroadcast.io/abr_corp/{name}/"

            processed_lines = []
            for line in stream_response.text.splitlines():
                line = line.strip()
                if not line:
                    continue

                if line.startswith("#"):
                    if "URI=" in line or "URL=" in line:
                        def fix_url(match_obj):
                            prefix = match_obj.group(1)
                            val = match_obj.group(2)
                            quote = match_obj.group(3)

                            if not val.startswith(("http://", "https://")):
                                val = base_url + val
                            return f"{prefix}{val}{quote}"

                        line = re.sub(r'((?:URI|URL)=["\']?)([^"\']*)(["\']?)', fix_url, line)
                    processed_lines.append(line)
                else:
                    if not line.startswith(("http://", "https://")):
                        line = base_url + line
                    
                    if ".m3u8" in line and "?" not in line:
                        line = f"{line}?{custom_token_query}"

                    processed_lines.append(line)

            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            with open(output_file, "w", encoding="utf-8") as f:
                f.write("\n".join(processed_lines))

            print(f"Başarıyla kaydedildi: {output_file}")

    except Exception as e:
        print(f"Hata oluştu ({embed_url}): {e}")
