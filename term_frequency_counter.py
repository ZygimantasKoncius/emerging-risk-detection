from collections import Counter
import pandas as pd
import nltk
from nltk.stem.porter import PorterStemmer
from datetime import datetime

start=datetime.now()

df = pd.read_csv('fullmetadatafinal1.csv')
df_filtered = df[(df['endIdx'] - df['startIdx'] > 1000) & (df['endIdx'] - df['startIdx'] < df['filelength']/3)]

# df_filtered = df_filtered.head(1000)
counter = Counter()
stemmer = PorterStemmer()
for index, row in df_filtered.iterrows():
    with open('risk_sections/' + row['filename']) as f:
        text = nltk.trigrams(nltk.word_tokenize(f.read().lower()))
        # text = [stemmer.stem(word) for word in text]
        counter = counter + Counter(text)

    
    if index>10000:
        break

print(len(counter))

res_df = pd.DataFrame(list(counter.items()), columns=['word', 'count'])
res_df = res_df.sort_values(by='count', ascending=False)
print(res_df.head(50))

res_df.to_csv('tf-simple-trigrams.csv')

print(datetime.now() - start)