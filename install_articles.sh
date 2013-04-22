mkdir -p /usr/local/nuus
rm -rf /usr/local/nuus/articles
rm -rf /usr/local/nuus/common
cp -r common /usr/local/nuus
cp -r services/articles /usr/local/nuus
cp -f services/articles/nuus-articles.conf /etc/init
