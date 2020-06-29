import pandas as pd

csvs = ('tf-simple-stemmed.csv', 'idf-simple-stemmed.csv', 'tfidf-simple-stemmed.csv')


df_tfs = pd.read_csv(csvs[0])

df_idfs = pd.read_csv(csvs[1])
df_idfs.columns = ['word', 'idf']
# df_idfs['word'] = df_idfs['word'].apply(lambda x: str(tuple(x.split())))

df_joined = pd.merge(df_tfs, df_idfs, on='word', how='inner')
df_joined['tfidf'] = df_joined['count']*df_joined['idf']
df_joined = df_joined.sort_values(by='tfidf', ascending=False)

df_joined.to_csv(csvs[2])

print(df_joined)