mkdir -p /usr/local/nuus
rm -rf /usr/local/nuus/feedcollector
rm -rf /usr/local/nuus/common
cp -r common /usr/local/nuus
cp -r feedcollector /usr/local/nuus
cp -f feedcollector/nuus-feedcollector.conf /etc/init
