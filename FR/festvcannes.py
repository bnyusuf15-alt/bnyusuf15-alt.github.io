import os
import requests

playlist_url = "https://hdfauth.ftven.fr/esi/TA?url=https://live-event.ftven.fr/out/v1/64bfbfd7f96c40b3989b029663be3e6d/index_france-domtom.m3u8"
output_file = "FR/festvcannes.m3u8"

# Download playlist
response = requests.get(playlist_url)
response.raise_for_status()

lines = response.text.splitlines()

stream_url = response.text

os.makedirs(os.path.dirname(output_file), exist_ok=True)

with open(output_file, "w", encoding="utf-8") as f:
    f.write(#EXTM3U)
    f.write(#EXT-X-STREAM-INF:BANDWIDTH=7680000)
    f.write(stream_url)

print(f"Saved to {output_file}")
