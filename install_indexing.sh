rm -rf /usr/local/nuus
mkdir /usr/local/nuus
cp -r common /usr/local/nuus
cp -r services/indexing /usr/local/nuus
cp -f services/indexing/nuus-indexing.conf /etc/init
