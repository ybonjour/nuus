mkdir -p /usr/local/nuus
rm -rf /usr/local/nuus/feeds
rm -rf /usr/local/nuus/common
cp -r common /usr/local/nuus
cp -r services/feeds /usr/local/nuus
cp -f services/feeds/nuus-feeds.conf /etc/init
