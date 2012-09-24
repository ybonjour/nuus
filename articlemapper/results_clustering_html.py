from database import Database
from similarity import Similarity

def htmlSimilarityMatrix(db, similarity):
    html = "<table border=1>"
    articles = [id for (id,) in db.iterQuery("SELECT Id FROM article")]
    print len(articles)
    html += "<tr><td>&nbsp;</td>"
    for article in articles:
        print article
        html += "<td><b>{0}</b></td>".format(article)
    html += "</tr>"
    
    
    for article1 in articles:
        print article1
        html += "<tr><td><b>{0}</b></td>".format(article1)
        for article2 in articles:
            print article2
            html += "<td>{0:2f}</td>".format(similarity.articleSimilarity(article1, article2))
        html += "</tr>"
    html += "</table>"
    return html
    
def htmlClusters(db, similarity):
    html = "<table border=1>"
    for (cluster,) in db.iterQuery("SELECT id FROM cluster"):
        html += "<tr><td><b>{0}</b></td>".format(cluster)
        html += "<td>{0}</td>".format(",".join(str(article) for (article,) in db.iterQuery("SELECT Id FROM article WHERE Cluster=%s", cluster)))
        html += "</tr>"
    html += "</table>"
    return html
        
db = Database()
db.connect()
try:
    similarity = Similarity(db)
    with open('clustering.html', 'w') as file:
        file.write("<html><head><title>Clustering</title></head><body>")
        file.write(htmlSimilarityMatrix(db, similarity))
        file.write(htmlClusters(db, similarity))
        file.write("<img src=\"clusters.png\" />")
        file.write("</body></html>")    
finally:
    db.close()



