import pandas as pd
import numpy as np

df = pd.read_csv('dataset.csv')
#select specified columns
feature = ['proto', 'service', 'id.resp_p', 'missed_bytes', 'version', 'cipher', 'curve',
    'resumed', 'last_alert', 'established', 'sni_matches_cert', 'username', 'password', 'certificate.not_valid_before',
    'certificate.not_valid_after', 'certificate.key_alg', 'certificate.sig_alg',
    'certificate.key_length']
df = df[feature]
#data type handle
df['id.resp_p'] = df['id.resp_p'].astype('Int64')
df['certificate.not_valid_after'] = pd.to_datetime(df['certificate.not_valid_after'], unit='s')
df['certificate.not_valid_before'] = pd.to_datetime(df['certificate.not_valid_after'], unit='s')
df['missed_bytes'] = df['missed_bytes'].astype('Int64')
print(df.info())
