mkdir -p /usr/local/nuus
rm -rf /usr/local/nuus/indexing
rm -rf /usr/local/nuus/common
cp -r common /usr/local/nuus
cp -r services/indexing /usr/local/nuus
cp -f services/indexing/nuus-indexing.conf /etc/init
