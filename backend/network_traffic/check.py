import pandas as pd
import numpy as np
from datetime import datetime


df = pd.read_csv('clean_dataset.csv')
print(df['proto'].value_counts())
print(df['service'].value_counts())
print(df['id.resp_p'].value_counts())
