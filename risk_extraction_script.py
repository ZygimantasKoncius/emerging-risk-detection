import pandas as pd
import re
import html
import os
import lxml.html
import lxml.html.clean
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

#all_df = all_df[all_df['filename']=='99780_2012-12-31_2013-02-21_10-K_0000099780-13-000019.txt']

cleanRe = re.compile('<(.|\n)*?>')
nbspRe = re.compile('&nbsp;|&#32;')
doubleSpacingRe = re.compile('  ')

def remove_html(text):
    """Remove html tags from a string"""
    return html.unescape(re.sub(doubleSpacingRe, ' ', re.sub(nbspRe, ' ', text)))

meta_data = []

for index, statement in all_df.iterrows():
    try:
        filename = statement['filename']
        # print(filename)
        text = ''

        start = statement['sectionstart']
        end = statement['sectionend']
        
        start = ' '.join(start.split())
        end = ' '.join(end.split())

        # with open(dataset_location + '/' + statement['filename']) as f:
        #     doc = f.read()

        # doc = lxml.html.fromstring(doc)    
        # text = "\n".join(map(lambda line: ' '.join(line.split()), doc.text_content().splitlines()))
        # text = " ".join(doc.text_content().split())
        # text = text[7000:]
        # text = remove_html(text)
        # with open('nohtml/'+filename, 'w') as f:
        #     f.write(text)
        # text = text[7000:]
        with open('nohtml/'+statement['filename']) as f:
            text = f.read()
        
        # startIdx = text.find(start)
        # endIdx = text.find(end)

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

        # while endIdx - startIdx < 500:
        #     text = text[endIdx:]
        #     startIdx = text.find(start)
        #     endIdx = text.find(end)

        # if endIdx<startIdx:
        #     startIdx = text.find(start)

        meta_data.append([filename,  startIdx, endIdx, start, end])

        with open('risk_sections/' + filename, 'w') as f:
            f.write(text[startIdx:endIdx])
    except:
        print(statement['filename'])
        print(traceback.print_exc())
        continue

meta_df = pd.DataFrame(meta_data, columns=['filename', 'startIdx', 'endIdx', 'startTerm', 'endTerm'])
meta_df.to_csv('metadata.csv')