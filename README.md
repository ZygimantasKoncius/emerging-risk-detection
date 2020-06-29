# Emerging Risk Detection In Financial Documents(Final Year Project)

The pipeline for processing documents and detecting topics

## Prerequisites

Python3, pip.
You might need to install some python dependencies from pip. Any part of the pipeline is runnable as python3 script, assuming you have data in appropriate folders and files.

## Dataset

The risk sections for the project are added in risk_section directory, they are extracted from the provided full dataset of 10K filings, parsed html and extracted risk sections.

## Pipeline scripts

```bash
html_parser.py # parses html documents to plain text
risk_section_extractor.py # extracts item 1A. risk section, requires RiskFactors_StartEnd.csv
risk_section_extraction_validator.py # simple verifier of the extracted risk sections
stopword-remover.py # removes stopwords
term_frequency_counter.py # tf counting for side exploration
idf-words.py # idf for words
tfid_dataframe_joiner.py # making tfidf dataframe from tf and idf outputs
tfidf-classifier.py # classify sentences using tf-idf into existing topics from topics_with_frequency.txt
sentence-clustering.py # various clustering approaches using word embeddings
topic_modelling.py # LDA topic modelling from various data clusterings
```
