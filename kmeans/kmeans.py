import numpy as np
import pandas as pd 
import matplotlib

from sklearn.cluster import KMeans

dataset=pd.read_json('data.json')
dataset.describe()

print(dataset.device_id)

# X = dataset.iloc[:, [3, 4]].values

# kmeans = KMeans(n_clusters = 3, init = 'random')


# print( kmeans.fit(X) )


# print (kmeans.cluster_centers_ )

# # print(X)

