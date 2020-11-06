import pandas pd
import numpy as np
from matplotlib import pyplot as plt

# Read csv 
data = pd.read_csv('./data/data.csv', sep=';')

data.info()

# Take category and saldo
cat_money = data[['category', 'saldo']]

from sklearn.cluster import KMeans

kmeans = KMeans(n_clusters=7)