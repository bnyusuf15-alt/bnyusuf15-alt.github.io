import os
import re
import requests

headers = {
    "User-Agent": "SmartOsTV",
    "Accept-Encoding": "identity",
}

# N12 (Akamai - profil kesmesi olmadan, direkt base ve master yapısı) ve K12/K12cc (CloudFront) kanal yapılandırmaları
channels = {
    "n12": {
        "cdn": "AKAMAI",
        "ticket_url": (
            "https://mass.mako.co.il/ClicksStatistics/entitlementsServicesV2.jsp"
            "?et=ngt"
            "&lp=https://mako-streaming.akamaized.net/stream/hls/live/20000821/k12n12wad/index.m3u8?b-in-range=0-800&user_id=5053dd0ad19b31b42f1daf2e631811f7"
            "&rv=AKAMAI"
        ),
        "master": "https://mako-streaming.akamaized.net/stream/hls/live/20000821/k12n12wad/index.m3u8?b-in-range=0-1800&user_id=5053dd0ad19b31b42f1daf2e631811f7&",
        "base": "https://mako-streaming.akamaized.net/stream/hls/live/20000821/k12n12wad/",
    },
    "k12": {
        "cdn": "AWS",
        "ticket_url": (
            "https://mass.mako.co.il/ClicksStatistics/entitlementsServicesV2.jsp"
            "?et=ngt"
            "&lp=/stream/hls/live/2033791/k12/index.m3u8?as=1"
            "&rv=AWS"
        ),
        "master": "https://d2249b6f08tjt0.cloudfront.net/k12/index.m3u8?b-in-range=0-5000&",
        "base": "https://d2249b6f08tjt0.cloudfront.net/k12/",
    },
    "k12cc": {
        "cdn": "AWS",
        "ticket_url": (
            "https://mass.mako.co.il/ClicksStatistics/entitlementsServicesV2.jsp"
            "?et=ngt"
            "&lp=/k12cc/index.m3u8?b-in-range=0-5000"
            "&rv=AWS"
        ),
        "master": "https://d2249b6f08tjt0.cloudfront.net/k12cc/index.m3u8?b-in-range=0-5000&",
        "base": "https://d2249b6f08tjt0.cloudfront.net/k12cc/",
    },
}

os.makedirs("IS2/", exist_ok=True)
s = requests.Session()

for name, info in channels.items():
    # 1. API üzerinden bilet ve güvenlik token'ını çekme
    ticket_response = s.get(info["ticket_url"], headers=headers)
    ticket_response.raise_for_status()
    raw_ticket = ticket_response.json()["tickets"][0]["ticket"]

    # 2. CDN türüne göre token ayıklama (Akamai için hdnea, AWS için direkt bilet)
    if info["cdn"] == "AKAMAI":
        pattern = r"hdnea=st%3D\d+%7Eexp%3D\d+%7Eacl%3D[^~]+%7Ehmac%3D[a-fA-F0-9]+"
        match = re.search(pattern, raw_ticket)
        if match:
            toki = match.group(0)
        else:
            raise ValueError(f"{name} için geçerli Akamai hdnea token bulunamadı!")
    else:
        toki = raw_ticket

    # 3. Master m3u8 indirme
    master_url = f"{info['master']}{toki}"
    response = s.get(master_url, headers=headers)
    response.raise_for_status()

    content = ""

    # 4. Satır bazlı işleme (N12 için profil kesmeden direkt base/master birleşimi, CloudFront için standart base yolu)
    for line in response.text.splitlines():
        line = line.strip()

        if not line:
            continue

        if line.startswith("#"):
            content += line + "\n"
        else:
            if info["cdn"] == "AKAMAI":
                # Profil manipülasyonu yapmadan, doğrudan base ve master URL yapısıyla satırları bağlama
                content += info["base"] + line + f"?{toki}\n"
            else:
                # AWS CloudFront için doğrudan base URL ile birleştirme
                content += info["base"] + line + "\n"

    with open(f"IS2/{name}.m3u8", "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Created IS2/{name}.m3u8")
