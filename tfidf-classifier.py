from collections import Counter
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

topics = []
with open('topics_with_frequency.txt') as f:
    i = -1
    for line in f:
        if 'topic' in line:
            if i > -1:
                topics[i] = topics[i][1:]
            i += 1
            topics.append('')
        else:
            line = line[2:]
            topics[i] += line.split(':')[0]

topics[-1] = topics[-1][1:]


start=datetime.now()

df = pd.read_csv('fullmetadatafinal1.csv')
df_filtered = df[(df['endIdx'] - df['startIdx'] > 1000) & (df['endIdx'] - df['startIdx'] < df['filelength']/3)]

df_filtered = df_filtered.head(100)
documents = topics
documentsRange = []
for index, row in df_filtered.iterrows():
    with open('nostopwords/' + row['filename']) as f:
        sentences = nltk.sent_tokenize(f.read())
    
    documentsRange.append((row['filename'], len(documents), len(documents) + len(sentences)))
    documents.extend(sentences)

vectorizer = TfidfVectorizer(use_idf=True)
vectors = vectorizer.fit_transform(documents)


def categorize(tfidf_matrix, index):
    cosine_similarities = linear_kernel(tfidf_matrix[index:index+1], tfidf_matrix[0:30]).flatten()
    related_docs_indices = [i for i in cosine_similarities.argsort()[::-1]]
    category_index = related_docs_indices[0]
    return (category_index, cosine_similarities[category_index])
    # return [(index, cosine_similarities[index]) for index in related_docs_indices]

countFail = 0
sum = 0
categorized_list = []
for doc in documentsRange:
    uncategorized = []
    print(doc)
    for i in range(doc[1], doc[2]):
        if len(documents[i].split()) > 5:
            categorization = categorize(vectors, i)

            sum += categorization[1]

            if categorization[1] < 0.05:
                countFail += 1
                uncategorized.append(documents[i])
            else:
                categorized_list.append({'sentence': documents[i], 'topic': categorization[0], 'similarity': categorization[1]})

    with open('demo_uncategorized/' + doc[0], 'w') as f:
        f.write(' '.join(uncategorized))

categorized_df = pd.DataFrame(categorized_list)
categorized_df.to_csv('demo-categorized-sentences.csv') 

print('Average similarity score: ' + str(sum/len(documents)))
print('Uncategorized sentences: ' + str(countFail))
print('Overall sentences: ' + str(len(documents)))
print('Uncategorized percentage: ' + str(countFail/len(documents)))

print(datetime.now() - start)
