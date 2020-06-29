import pandas as pd

df = pd.read_csv('fullmetadatafinal1.csv')
df_filtered = df[(df['endIdx'] - df['startIdx'] > 1000) & (df['endIdx'] - df['startIdx'] < df['filelength']/3)]

haveStaffComments = 0

for index, row in df_filtered.iterrows():
    with open('risk_sections/' + row['filename']) as f:
        text = f.read()
    
    text = text[-200:]
    text = text.lower()
    if 'unresolved staff comments' in text:
        haveStaffComments += 1
    # else:
    #     print(row['endTerm'])
    #     print(row['filename'])

print(len(df_filtered))
print(haveStaffComments)