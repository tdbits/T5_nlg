import glob
import os
import re
import xml.etree.ElementTree as ET
import pandas as pd
import sys

TRAIN_DIR = sys.argv[1]
OUTPUT_DIR = sys.argv[2]

files = []

for root, dirs, file_names in os.walk(TRAIN_DIR):
    for file_name in file_names:
        if file_name.endswith('.xml'):
            files.append(os.path.join(root, file_name))

print(f"{len(files)} files found.")

triple_re=re.compile('(\d)triples')
data_dct={}
for file in files:
    print(file)
    tree = ET.parse(file)
    root = tree.getroot()
    triples_num=int(triple_re.findall(file)[0])
    for sub_root in root:
        for ss_root in sub_root:
            strutured_master=[]
            unstructured=[]
            for entry in ss_root:
                unstructured.append(entry.text)
                strutured=[triple.text for triple in entry]
                strutured_master.extend(strutured)
            unstructured=[i for i in unstructured if i.replace('\n','').strip()!='' ]
            strutured_master=strutured_master[-triples_num:]
            strutured_master_str=(' && ').join(strutured_master)
            data_dct[strutured_master_str]=unstructured
print("Constructing dataframe.")
mdata_dct={"prefix":[], "input_text":[], "target_text":[]}
for st,unst in data_dct.items():
    for i in unst:
        mdata_dct['prefix'].append('webNLG')
        mdata_dct['input_text'].append(st)
        mdata_dct['target_text'].append(i)


df=pd.DataFrame(mdata_dct)
df.to_csv(os.path.join(OUTPUT_DIR, 'webNLG2020_train.csv'))
