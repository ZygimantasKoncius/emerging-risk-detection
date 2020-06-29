import pandas as pd
import re
import html
import os
import lxml.html
import traceback

dataset_location = 'full_dataset' # '10k20f_15' for local
# dataset_location = '10k20f_15'
risk_section_df = pd.read_csv('RiskFactors_StartEnd.csv')
risk_section_df['periodofreport'] = risk_section_df['periodofreport'].apply(pd.to_datetime)
risk_section_df['filingdate'] = risk_section_df['filingdate'].apply(pd.to_datetime)
files_df = pd.DataFrame(os.listdir(dataset_location), columns=['filename'])
files_df[['cik', 'periodofreport', 'filingdate', 'documenttype', 'ending']] = files_df['filename'].str.split('_', expand=True)
files_df['cik'] = files_df['cik'].apply(pd.to_numeric)
files_df['periodofreport'] = files_df['periodofreport'].apply(pd.to_datetime)
files_df['filingdate'] = files_df['filingdate'].apply(pd.to_datetime)

all_df = risk_section_df.merge(files_df, on=['cik', 'documenttype', 'periodofreport', 'filingdate'], how='left')
all_df = all_df[all_df['filename'].notnull()]

meta_data = []

for index, statement in all_df.iterrows():
    try:
        filename = statement['filename']

        with open(dataset_location + '/' + statement['filename']) as f:
            doc = f.read()

        doc = lxml.html.fromstring(doc)    
        text = " ".join(doc.text_content().split())
        with open('nohtml/'+filename, 'w') as f:
            f.write(text)
            
    except:
        print(statement['filename'])
        print(traceback.print_exc())
        continue

meta_df = pd.DataFrame(meta_data, columns=['filename', 'startIdx', 'endIdx', 'startTerm', 'endTerm'])
meta_df.to_csv('metadata.csv')