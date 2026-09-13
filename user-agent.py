import re
import urllib.request

# M3U dosyasının bulunduğu URL
url = "https://raw.githubusercontent.com/Paradise-91/ParaTV/refs/heads/main/playlists/paratv/main/paratv.m3u"

try:
    print("M3U dosyası indiriliyor...")
    # URL'den m3u içeriğini indiriyoruz
    with urllib.request.urlopen(url) as response:
        m3u_content = response.read().decode("utf-8")

    # 1. Aşama: #EXTVLCOPT:http-user-agent= kısmından sonrasını yakalamak için regex
    # (Parantez grubu () kullanarak sadece eşittirden sonraki değeri hedefliyoruz)
    pattern_extract = r"^#EXTVLCOPT:http-user-agent=(.*)$"
    
    # re.findall ile tüm eşleşen user-agent değerlerini liste olarak alıyoruz
    user_agents = re.findall(pattern_extract, m3u_content, re.MULTILINE)

    if user_agents:
        # Listebin ilk elemanını alıyoruz (İlk user agent)
        first_user_agent = user_agents[0].strip()
        
        # user_agent.txt dosyasına kaydediyoruz
        with open("user_agent.txt", "w", encoding="utf-8") as ua_file:
            ua_file.write(first_user_agent)
            
        print(f"[BAŞARILI] Bulunan ilk User-Agent 'user_agent.txt' dosyasına kaydedildi:\n-> {first_user_agent}")
    else:
        print("[BİLGİ] Dosyada eşleşen herhangi bir User-Agent bulunamadı.")

    print("-" * 50)

    # 2. Aşama: re.sub ile #EXTVLCOPT:http-user-agent= kısmını ve değerini boş yapmak
    # Tüm satırı veya ilgili kısmı tamamen boşluk/hiçlik ile değiştiriyoruz
    pattern_sub = r"^#EXTVLCOPT:http-user-agent=.*$"
    
    # re.sub ile eşleşen tüm satırları boş string ('') ile değiştiriyoruz
    cleaned_content = re.sub(pattern_sub, "", m3u_content, flags=re.MULTILINE)

    print(f"[BAŞARILI] User-Agent satırları temizlendi.'")

except Exception as e:
    print(f"[HATA] İşlem sırasında bir hata oluştu: {e}")
