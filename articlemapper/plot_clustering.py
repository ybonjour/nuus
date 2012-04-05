import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')

from matplotlib import pyplot as plt
from database import Database
from similarity import Similarity

db = Database()
db.connect()
try:
    fig = plt.figure()
    ax = fig.add_subplot(111)
    similarity = Similarity(db)
    clusterNr = 1
    
    totalAverage = similarity.averageWordImportanceDict([articleId for (articleId,) in db.iterQuery("SELECT id FROM article")])
    #zeroVector = {}
    for (clusterId, centroid) in db.iterQuery("SELECT Id, Centroid FROM cluster"):
        #distances = [similarity.distanceToVector(article, zeroVector) for (article,) in db.iterQuery("SELECT Id FROM article WHERE Cluster=%s", clusterId)]
        #ax.plot([clusterNr]*len(distances), distances, 'o')

        similarities = [similarity.similarityToVector(article, totalAverage) for (article,) in db.iterQuery("SELECT Id FROM article WHERE Cluster=%s", clusterId)]
        ax.plot([clusterNr]*len(similarities), similarities, 'o')
        
        #Plot average
        average = similarity.averageWordImportanceDict([articleId for (articleId,) in db.iterQuery("SELECT Id FROM article WHERE Cluster=%s", clusterId)])
        ax.plot([clusterNr], [similarity.similarity(average, totalAverage)], '-o')
        
        # centroidQuery = "SELECT Id FROM article WHERE Id=%s"
        # centroid = db.uniqueScalarOrZero(centroidQuery, centroid)
        # ax.plot([clusterNr], [similarity.distanceToVector(centroid, zeroVector)], '-o')

        clusterNr += 10
    ax.set_title('Clusters')
    plt.savefig('clusters.png')
    #plt.show()
    
finally:
    db.close()



