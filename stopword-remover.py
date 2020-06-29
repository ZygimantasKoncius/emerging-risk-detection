from nltk.corpus import stopwords
import pandas as pd
from datetime import datetime

stops = set(stopwords.words('english'))

start=datetime.now()

df = pd.read_csv('fullmetadatafinal1.csv')
df_filtered = df[(df['endIdx'] - df['startIdx'] > 1000) & (df['endIdx'] - df['startIdx'] < df['filelength']/3)]

for index, row in df_filtered.iterrows():
    with open('risk_sections/' + row['filename']) as f:
        document = f.read()

    text = [word for word in document.split() if word.lower() not in stops]

    with open('nostopwords/' + row['filename'], 'w') as f:
        f.write(' '.join(text))

print(datetime.now() - start)