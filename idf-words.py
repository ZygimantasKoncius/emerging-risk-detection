from collections import Counter
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

start=datetime.now()

df = pd.read_csv('fullmetadatafinal1.csv')
df_filtered = df[(df['endIdx'] - df['startIdx'] > 1000) & (df['endIdx'] - df['startIdx'] < df['filelength']/3)]

# df_filtered = df_filtered.head(1000)
# documentsRange = []
documents = []
stemmer = PorterStemmer()
for index, row in df_filtered.iterrows():
    with open('risk_sections/' + row['filename']) as f:
        document = f.read().lower()
        # document = ' '.join([stemmer.stem(word) for word in nltk.word_tokenize(f.read().lower())])

    if index % 1000 == 0:
        print(row['filename'])
        print(index)
        print(datetime.now() - start)
    
    # documentsRange.append((row['filename'], len(documents), len(documents) + len(sentences)))
    documents.append(document)

vectorizer = TfidfVectorizer(use_idf=True, smooth_idf=False, ngram_range=(3, 3))
tfidf_matrix = vectorizer.fit_transform(documents)
df_idf = pd.DataFrame(vectorizer.idf_, index = vectorizer.get_feature_names(), columns = ['idf'])
df_idf['idf'] = df_idf['idf'] - 1
print(df_idf)


df_idf.to_csv('idf-simple-trigrams.csv')

print(datetime.now() - start)
