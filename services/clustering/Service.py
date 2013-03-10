__author__ = 'Yves Bonjour'

from Clusterer import Clusterer
from Clusterer import MemoryClusterStore
from VectorCalculator import VectorCalculator
from Indexer import Indexer

if __name__ == "__main__":
    indexer = Indexer()
    calculator = VectorCalculator(indexer)
    centroid_store = MemoryClusterStore([])
    clusterer = Clusterer(centroid_store, calculator)