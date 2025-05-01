import pickle
import pandas as pd


model = pickle.load(open('../model/RandomForestModel.sav', 'rb'))
df = pd.read_csv('./clean_dataset.csv')
print(df)
df = df.drop(['Unnamed: 0', 'secure_label'], axis=1)
print(model.predict(df)[0])
