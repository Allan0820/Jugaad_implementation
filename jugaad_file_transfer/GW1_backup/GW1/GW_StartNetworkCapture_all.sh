rm -rf ~/trafficLogs
mkdir ~/trafficLogs
chmod 777 ~/trafficLogs


tshark -i eno1 -T fields -e tcp.dstport -e _ws.col.Protocol -e frame.len -e frame.time_delta -e ssl.handshake.version -e ssl.handshake.certificate -e ssl.handshake.extensions_server_name -e dns.qry.name -e dns.a -e dns.resp.name -e dns.count.answers -e http.request.full_uri -e http.file_data -e frame.time -E header=y -E separator=, -E quote=d -E occurrence=f > ~/trafficLogs/eno1_$1.csv &
tshark -i enp1s0 -T fields -e tcp.dstport -e _ws.col.Protocol -e frame.len -e frame.time_delta -e ssl.handshake.version -e ssl.handshake.certificate -e ssl.handshake.extensions_server_name -e dns.qry.name -e dns.a -e dns.resp.name -e dns.count.answers -e http.request.full_uri -e http.file_data -e frame.time -E header=y -E separator=, -E quote=d -E occurrence=f > ~/trafficLogs/enp1s0_$1.csv &
tshark -i enp2s0 -T fields -e tcp.dstport -e _ws.col.Protocol -e frame.len -e frame.time_delta -e ssl.handshake.version -e ssl.handshake.certificate -e ssl.handshake.extensions_server_name -e dns.qry.name -e dns.a -e dns.resp.name -e dns.count.answers -e http.request.full_uri -e http.file_data -e frame.time -E header=y -E separator=, -E quote=d -E occurrence=f > ~/trafficLogs/enp2s0_$1.csv &



#tshark -i enp1s0 -w ~/trafficLogs/enp1s0_$1.pcap &
#tshark -i enp2s0 -w ~/trafficLogs/enp2s0_$1.pcap &

echo "Tshark started on Gateway 2 and processes are moved to the background" &


