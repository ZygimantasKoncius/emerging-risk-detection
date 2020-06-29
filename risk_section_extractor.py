import pandas as pd
import re
import os
import traceback

dataset_location = 'nohtml'
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

        start = statement['sectionstart']
        end = statement['sectionend']
        
        start = ' '.join(start.split())
        end = ' '.join(end.split())

        with open('nohtml/' + statement['filename']) as f:
            text = f.read()


        startIdxArr = [detected.start() for detected in re.finditer(start, text)]
        endIdxArr = [detected.start() for detected in re.finditer(end, text)]
        startIdx = -1
        endIdx = -1
        for starti in startIdxArr:
            for endi in endIdxArr:
                if endi > starti:
                    if endi == endIdx and startIdx<starti or endi - starti > endIdx - startIdx:
                        startIdx = starti
                        endIdx = endi
                    break

        meta_data.append([filename, len(text), startIdx, endIdx, start, end])

        with open('risk_sections/' + filename, 'w') as f:
            f.write(text[startIdx:endIdx])
    except:
        print(statement['filename'])
        print(traceback.print_exc())
        continue

meta_df = pd.DataFrame(meta_data, columns=['filename', 'filelength','startIdx', 'endIdx', 'startTerm', 'endTerm'])
meta_df.to_csv('metadata.csv')