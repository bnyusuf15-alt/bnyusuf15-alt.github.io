#!/bin/bash

NEW_AUTH=$(wget -qO- https://services.iol.pt/matrix?userId)

if [ -z "$NEW_AUTH" ]; then
  echo "API'den wmsAuthSign değeri alınamadı!"
  exit 1
fi

mkdir -p res/26-2

cat << EOF > PT/cnnpt.m3u8
#EXTM3U
#EXT-X-VERSION:3
#EXT-X-STREAM-INF:BANDWIDTH=1393632,RESOLUTION=1280x720,CODECS="avc1.64001f,mp4a.40.2"
https://video-auth1.iol.pt/live_cnn/live_cnn/edge_servers/cnn-720p/chunks.m3u8?wmsAuthSign=${NEW_AUTH}
#EXT-X-STREAM-INF:BANDWIDTH=871507,RESOLUTION=854x480,CODECS="avc1.66.30,mp4a.40.2"
https://video-auth1.iol.pt/live_cnn/live_cnn/edge_servers/cnn-480p/chunks.m3u8?wmsAuthSign=${NEW_AUTH}
#EXT-X-STREAM-INF:BANDWIDTH=576951,RESOLUTION=640x360,CODECS="avc1.66.30,mp4a.40.2"
https://video-auth1.iol.pt/live_cnn/live_cnn/edge_servers/cnn-360p/chunks.m3u8?wmsAuthSign=${NEW_AUTH}
#EXT-X-STREAM-INF:BANDWIDTH=346578,RESOLUTION=426x240,CODECS="avc1.42c015,mp4a.40.2"
https://video-auth1.iol.pt/live_cnn/live_cnn/edge_servers/cnn-240p/chunks.m3u8?wmsAuthSign=${NEW_AUTH}
EOF

cat << EOF > PT/tvi.m3u8
#EXTM3U
#EXT-X-VERSION:3
#EXT-X-STREAM-INF:BANDWIDTH=1972967,RESOLUTION=1280x720,CODECS="avc1.640029,mp4a.40.2"
https://video-auth7.iol.pt/live_tvi/live_tvi/edge_servers/tvi-720p/chunks.m3u8?wmsAuthSign=${NEW_AUTH}
#EXT-X-STREAM-INF:BANDWIDTH=845169,RESOLUTION=854x480,CODECS="avc1.66.30,mp4a.40.2"
https://video-auth7.iol.pt/live_tvi/live_tvi/edge_servers/tvi-480p/chunks.m3u8?wmsAuthSign=${NEW_AUTH}
#EXT-X-STREAM-INF:BANDWIDTH=565523,RESOLUTION=640x360,CODECS="avc1.66.30,mp4a.40.2"
https://video-auth7.iol.pt/live_tvi/live_tvi/edge_servers/tvi-360p/chunks.m3u8?wmsAuthSign=${NEW_AUTH}
#EXT-X-STREAM-INF:BANDWIDTH=345862,RESOLUTION=426x240,CODECS="avc1.42c015,mp4a.40.2"
https://video-auth7.iol.pt/live_tvi/live_tvi/edge_servers/tvi-240p/chunks.m3u8?wmsAuthSign=${NEW_AUTH}
EOF

cat << EOF > PT/tvificcao.m3u8
#EXTM3U
#EXT-X-VERSION:3
#EXT-X-STREAM-INF:BANDWIDTH=1393632,RESOLUTION=1280x720,CODECS="avc1.64001f,mp4a.40.2"
https://video-auth8.iol.pt/live_tvi_ficcao/live_tvi_ficcao/edge_servers/tvificcao-720p/chunks.m3u8?wmsAuthSign=${NEW_AUTH}
#EXT-X-STREAM-INF:BANDWIDTH=871507,RESOLUTION=854x480,CODECS="avc1.66.30,mp4a.40.2"
https://video-auth8.iol.pt/live_tvi_ficcao/live_tvi_ficcao/edge_servers/tvificcao-480p/chunks.m3u8?wmsAuthSign=${NEW_AUTH}
#EXT-X-STREAM-INF:BANDWIDTH=576951,RESOLUTION=640x360,CODECS="avc1.66.30,mp4a.40.2"
https://video-auth8.iol.pt/live_tvi_ficcao/live_tvi_ficcao/edge_servers/tvificcao-360p/chunks.m3u8?wmsAuthSign=${NEW_AUTH}
#EXT-X-STREAM-INF:BANDWIDTH=346578,RESOLUTION=426x240,CODECS="avc1.42c015,mp4a.40.2"
https://video-auth8.iol.pt/live_tvi_ficcao/live_tvi_ficcao/edge_servers/tvificcao-240p/chunks.m3u8?wmsAuthSign=${NEW_AUTH}
EOF

cat << EOF > PT/tviint.m3u8
#EXTM3U
#EXT-X-VERSION:3
#EXT-X-STREAM-INF:BANDWIDTH=2225412,RESOLUTION=1280x720,CODECS="avc1.640029,mp4a.40.2"
https://video-auth7.iol.pt/live_tvi_internacional/live_tvi_internacional/edge_servers/tviinternacional-720p/chunks.m3u8?wmsAuthSign=${NEW_AUTH}
#EXT-X-STREAM-INF:BANDWIDTH=991382,RESOLUTION=854x480,CODECS="avc1.66.30,mp4a.40.2"
https://video-auth7.iol.pt/live_tvi_internacional/live_tvi_internacional/edge_servers/tviinternacional-480p/chunks.m3u8?wmsAuthSign=${NEW_AUTH}
#EXT-X-STREAM-INF:BANDWIDTH=659926,RESOLUTION=640x360,CODECS="avc1.66.30,mp4a.40.2"
https://video-auth7.iol.pt/live_tvi_internacional/live_tvi_internacional/edge_servers/tviinternacional-360p/chunks.m3u8?wmsAuthSign=${NEW_AUTH}
#EXT-X-STREAM-INF:BANDWIDTH=393711,RESOLUTION=426x240,CODECS="avc1.42c015,mp4a.40.2"
https://video-auth7.iol.pt/live_tvi_internacional/live_tvi_internacional/edge_servers/tviinternacional-240p/chunks.m3u8?wmsAuthSign=${NEW_AUTH}
EOF

cat << EOF > PT/tvimai.m3u8
#EXTM3U
#EXT-X-VERSION:3
#EXT-X-STREAM-INF:BANDWIDTH=1393632,RESOLUTION=1280x720,CODECS="avc1.64001f,mp4a.40.2"
https://video-auth8.iol.pt/live_vmais/live_vmais/edge_servers/vmais-720p/chunks.m3u8?wmsAuthSign=${NEW_AUTH}
#EXT-X-STREAM-INF:BANDWIDTH=871507,RESOLUTION=854x480,CODECS="avc1.66.30,mp4a.40.2"
https://video-auth8.iol.pt/live_vmais/live_vmais/edge_servers/vmais-480p/chunks.m3u8?wmsAuthSign=${NEW_AUTH}
#EXT-X-STREAM-INF:BANDWIDTH=576951,RESOLUTION=640x360,CODECS="avc1.66.30,mp4a.40.2"
https://video-auth8.iol.pt/live_vmais/live_vmais/edge_servers/vmais-360p/chunks.m3u8?wmsAuthSign=${NEW_AUTH}
#EXT-X-STREAM-INF:BANDWIDTH=346578,RESOLUTION=426x240,CODECS="avc1.42c015,mp4a.40.2"
https://video-auth8.iol.pt/live_vmais/live_vmais/edge_servers/vmais-240p/chunks.m3u8?wmsAuthSign=${NEW_AUTH}
EOF

cat << EOF > PT/tvireality.m3u8
#EXTM3U
#EXT-X-VERSION:3
#EXT-X-STREAM-INF:BANDWIDTH=1972967,RESOLUTION=1280x720,CODECS="avc1.640029,mp4a.40.2"
https://video-auth4.iol.pt/live_tvi_reality/live_tvi_reality/edge_servers/tvireality-720_passthrough/chunks.m3u8?wmsAuthSign=${NEW_AUTH}
#EXT-X-STREAM-INF:BANDWIDTH=845169,RESOLUTION=854x480,CODECS="avc1.66.30,mp4a.40.2"
https://video-auth4.iol.pt/live_tvi_reality/live_tvi_reality/edge_servers/tvireality-480p/chunks.m3u8?wmsAuthSign=${NEW_AUTH}
#EXT-X-STREAM-INF:BANDWIDTH=565523,RESOLUTION=640x360,CODECS="avc1.66.30,mp4a.40.2"
https://video-auth4.iol.pt/live_tvi_reality/live_tvi_reality/edge_servers/tvireality-360p/chunks.m3u8?wmsAuthSign=${NEW_AUTH}
#EXT-X-STREAM-INF:BANDWIDTH=345862,RESOLUTION=426x240,CODECS="avc1.42c015,mp4a.40.2"
https://video-auth4.iol.pt/live_tvi_reality/live_tvi_reality/edge_servers/tvireality-240p/chunks.m3u8?wmsAuthSign=${NEW_AUTH}
EOF

echo "Tüm playlist dosyaları güncel token ile oluşturuldu."
exit 0
