mkdir -p /usr/local/nuus
rm -rf /usr/local/nuus/clustering
rm -rf /usr/local/nuus/common
cp -r common /usr/local/nuus
cp -r services/clustering /usr/local/nuus
cp -f services/clustering/nuus-clustering.conf /etc/init
