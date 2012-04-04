import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')

from matplotlib import pyplot as plt
from database import Database
from clustering import Article
from similarity import Similarity

db = Database()
db.connect()
try:
    fig = plt.figure()
    ax = fig.add_subplot(111)
    similarity = Similarity(db)
    clusterNr = 1
    for (clusterId, centroid) in db.iterQuery("SELECT Id, Centroid FROM cluster"):
        zeroVector = {}
        query = "SELECT Id, Title, content, Feed, Updated, Language FROM article WHERE Cluster=%s"
        distances = [similarity.distanceToVector(article, zeroVector) for article in
                    (Article._make(articleItem) for articleItem in db.iterQuery(query, clusterId))]

        ax.plot([clusterNr]*len(distances), distances, 'o')
        
        #Plot centroid
        centroidQuery = "SELECT Id, Title, content, Feed, Updated, Language FROM article WHERE Id=%s"
        centroid = Article._make(db.uniqueQuery(centroidQuery, centroid))
        ax.plot([clusterNr], [similarity.distanceToVector(centroid, zeroVector)], '-o')

        clusterNr += 10
    ax.set_title('Clusters')
    plt.savefig('clusters.png')
    #plt.show()
    
finally:
    db.close()



