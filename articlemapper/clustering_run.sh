python clustering_test.py
python results_clustering_plot.py
python results_clustering_html.py

mv clusters.png /var/www/nuus/clusters
mv clustering.html /var/www/nuus/clusters

chown www-data:www-data /var/www/nuus/clusters/clusters.png 
chown www-data:www-data /var/www/nuus/clusters/clustering.html
