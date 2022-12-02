#!/bin/bash

TMP_FILE='/tmp/vendors.txt'
FILE='vendors.txt'

curl -s 'https://directory.ifsecglobal.com/screens-monitors-code004843.html' | grep -E 'ed-companyName' | grep -E -o '">[^/]+<' | sed 's/<//' | sed 's/">//' > $TMP_FILE

for urlpath in cameras-code004815.html cctv-poles-and-columns-code004816.html cctv-poles-and-columns-code004816.html data-storage-solutions-code009685.html voice-video-integrated-data-systems-code004908.html dvr-code004822.html voice-video-integrated-data-storage-code004941.html nvr-code004827.html 4k-cameras-code009684.html anpr-code004813.html body-worn-cameras-code007865.html hd-quality-cameras-code007866.html low-light-level-camera-systems-code007867.html camera-housings-code004814.html internet-remote-surveillance-code004932.html cctv-monitoring-code004999.html dome-camera-code004821.html ip-cameras-code004823.html security-camera-lenses-code004824.html security-monitors-code004825.html security-screens-code007437.html ptz-camera-code004828.html switches-code004968.html remote-surveillance-code004829.html public-space-surveillance-code005012.html infrared-cameras-code007439.html thermal-imaging-code004833.html ai-machinelearning-code009668.html security-cameras-code007485.html video-surveillance-code007482.html video-surveillance-code004812.html
do
    curl -s "https://directory.ifsecglobal.com/$urlpath" | grep -E 'ed-companyName' | grep -E -o '">[^/]+<' | sed 's/<//' | sed 's/">//' >> $TMP_FILE
done
#curl -s '' | grep -E 'ed-companyName' | grep -E -o '">[^/]+<' | sed 's/<//' | sed 's/">//' >> $TMP_FILE


for letter in {A..Z} {2..5} {7..9}
do
    curl -s "https://www.ispyconnect.com/sources.aspx?letter=$letter" | grep -E -o 'man\.aspx\?n=[^"]{1,}"' | sed 's/man.aspx?n=//' | sed 's/"//' | while read -r line ; do
grep -E "$line " vendors.txt >> $TMP_FILE
    done
done


echo 'Tenda Technology Co., Ltd.' >> $TMP_FILE #https://www.google.com/search?q=Tenda+Technology+CCTV&tbm=isch
echo 'LG Innotek' >> $TMP_FILE #https://www.google.com/search?q=LG+Innotek+CCTV&tbm=isch
echo 'Hand Held Products Inc' >> $TMP_FILE #Handheld Thermal Cameras
echo 'Wistron Neweb Corporation' >> $TMP_FILE #https://www.wnc.com.tw/index.php?action=pro_detail&id=76
echo 'HangZhou KuoHeng Technology Co.,ltd' >> $TMP_FILE #https://www.google.com/search?q=HangZhou+KuoHeng+Technology&tbm=isch
echo 'VCS Video Communication Systems AG' >> $TMP_FILE
echo 'D-Link International' >> $TMP_FILE
echo 'Cisco-Linksys, LLC' >> $TMP_FILE
echo 'ICP Internet Communication Payment AG' >> $TMP_FILE
echo 'China Dragon Technology Limited' >> $TMP_FILE
echo 'SAMSUNG TECHWIN CO.,LTD' >> $TMP_FILE
echo 'Hanwha Techwin Security Vietnam' >> $TMP_FILE
echo 'Beward R&D Co., Ltd.' >> $TMP_FILE
echo 'Lorex Technology Inc.' >> $TMP_FILE
echo 'TP-LINK TECHNOLOGIES CO.,LTD.' >> $TMP_FILE
echo 'ABUS Security-Center GmbH & Co. KG' >> $TMP_FILE
echo 'ACM Systems' >> $TMP_FILE
echo 'Aztech Electronics Pte Ltd' >> $TMP_FILE
echo 'Axium Technologies, Inc.' >> $TMP_FILE
echo 'Ace Axis Limited' >> $TMP_FILE
echo 'Shenzhen Kezhonglong Optoelectronic Technology Co., Ltd' >> $TMP_FILE
#echo '' >> $TMP_FILE


echo "Total vendors in the list: "`cat $TMP_FILE | wc -l`
cat $TMP_FILE | sort| uniq > $FILE
echo "Unique vendors in the list: "`cat $FILE | wc -l`
