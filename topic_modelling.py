import pandas as pd
import nltk
import numpy as np
from datetime import datetime
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation as LDA

def print_topics(model, count_vectorizer, n_top_words):
    words = count_vectorizer.get_feature_names()
    for topic_idx, topic in enumerate(model.components_):
        print("\nTopic #%d:" % topic_idx)
        print(" ".join([words[i] for i in topic.argsort()[:-n_top_words - 1:-1]]))

start=datetime.now()

df = pd.read_csv('fullmetadataappended.csv')
df_filtered = df[(df['endIdx'] - df['startIdx'] > 1000) & (df['endIdx'] - df['startIdx'] < df['filelength']/3)]

def generateFirstOccurenceTopics():
    cluster_df = pd.read_csv('demo-sentence-clusters.csv')
    cluster_df = cluster_df[cluster_df['label'] != -1]
    first_df = cluster_df[cluster_df.groupby(['label'])['fyear'].transform(min) == cluster_df['fyear']]
    first_df = first_df[first_df['fyear']>2005]
    print(len(first_df))

    count_vectorizer = CountVectorizer(stop_words='english')
    count_data = count_vectorizer.fit_transform(cluster_df['sentence'])

    lda = LDA(n_components=10, n_jobs=-1)
    lda.fit(count_data)

    print_topics(lda, count_vectorizer, 10)

def generateYearTopics(year):
    files_df = df_filtered.head(100)
    if year:
        files_df = files_df[files_df['fyear']==year]
    
    print(year)

    documents = []
    for index, row in files_df.iterrows():
        with open('demo_uncategorized/' + row['filename']) as f:
            documents.append(f.read().lower())
    
    count_vectorizer = CountVectorizer(stop_words='english')
    count_data = count_vectorizer.fit_transform(documents)
    lda = LDA(n_components=10, n_jobs=-1)
    lda.fit(count_data)
    print_topics(lda, count_vectorizer, 10)

for year in range(2005, 2016):
    generateYearTopics(year)


print('\nWhole dataset topics\n')
generateYearTopics(False)

print('\nFirst mention topics\n')
generateFirstOccurenceTopics()

print(datetime.now() - start)