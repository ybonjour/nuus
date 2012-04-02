import clustering
import database
import similarity

db = database.Database()
db.connect()
try:
    similarity = similarity.Similarity(db)
    clusterer = clustering.Clusterer(similarity, db, 3)
    clusterer.clustering()
    db.commit()
finally:
    db.close()