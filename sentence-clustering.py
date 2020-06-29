import pandas as pd
import torch
import nltk
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity, cosine_distances
from datetime import datetime
from sklearn.cluster import DBSCAN, KMeans
from coclust.clustering import SphericalKmeans

start=datetime.now()

df = pd.read_csv('fullmetadataappended.csv')
df_filtered = df[(df['endIdx'] - df['startIdx'] > 1000) & (df['endIdx'] - df['startIdx'] < df['filelength']/3)]

embed = torch.load('10K-word-embeddings/10k_word_embeddings.tar')
vocab_to_int = torch.load('10K-word-embeddings/vocab_to_int.tar')

df_filtered = df_filtered.head(100)
sentenceVectors = []
for index, row in df_filtered.iterrows():
    with open('uncategorized/' + row['filename']) as f:
        sentences = nltk.sent_tokenize(f.read())

        for sentence in sentences:
            sentenceVectors.append((sentence, row['filename'], np.mean([embed[vocab_to_int[word]] for word in nltk.word_tokenize(sentence) if word in vocab_to_int], axis=0)))
    
sentenceVectorsDf = pd.DataFrame(sentenceVectors, columns=['sentence', 'filename', 'vector'])
sentencesDF = sentenceVectorsDf.merge(df_filtered, on='filename')[['sentence', 'filename', 'vector', 'fyear']]
print(len(sentencesDF))
print('Number of na: ' + str(len(sentencesDF) - len(sentencesDF.dropna())))
sentencesDF = sentencesDF.dropna().reset_index(drop=True)
vectorMatrix = np.concatenate(sentencesDF['vector'].to_numpy()).reshape(len(sentencesDF), 300)

# distance_matrix = cosine_distances(vectorMatrix)
# pd.DataFrame(similarity_matrix).to_csv('similarity-matrix.csv')
# pd.DataFrame(distance_matrix).to_csv('distance-matrix.csv')

# print(sentencesDF.head(20))
# print(sentencesDF)
# print(len(sentenceVectorsDf))


# kmeans = KMeans(n_clusters=50, n_jobs=-1)
# kclusters = kmeans.fit_predict(vectorMatrix)
# kClustersDF = sentencesDF.copy()
# kClustersDF['label'] = kclusters
# kClustersDF = kClustersDF.sort_values(by='label')
# print(np.where((vectorMatrix == kmeans.cluster_centers_[0]).all(axis=1)))

# for index, row in sentencesDF.iterrows():
#     if row['vector'] in kmeans.cluster_centers_:
#         print(row['sentence'])
# sentencesDF.drop(columns=['vector'], inplace=True)

# sKmeans = SphericalKmeans(n_clusters=30)
# sKmeans.fit(vectorMatrix)
# kClustersDF = sentencesDF.copy()
# kClustersDF['label'] = sKmeans.labels_
# kClustersDF = kClustersDF.sort_values(by='label')
# kClustersDF.to_csv('kmeans-clusters.csv')
# print(sKmeans.criterions)


clusters_df = pd.DataFrame(DBSCAN(eps=0.1, min_samples=2, metric='cosine', n_jobs=-1).fit_predict(vectorMatrix), columns=['label'])
clusters_df = clusters_df.merge(sentencesDF, left_index=True, right_index=True).sort_values(by='label')
print(clusters_df)
clusters_df.to_csv('demo-sentence-clusters.csv')



print(datetime.now() - start)