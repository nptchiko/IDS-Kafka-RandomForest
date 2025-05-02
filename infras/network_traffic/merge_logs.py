import pandas as pd
import numpy as np


PATH = '../../data/logs/'


def format_csv(input_file):
    with open(input_file, "r", encoding="utf-8") as file:
        lines = file.readlines()
    separator = "\t"
    columns = []
    data_rows = []
    current_line = ""
    for line in lines:
        if line.startswith("#separator"):
            continue
        elif line.startswith("#fields"):
            columns = line.split(separator)[1:]

            data_rows.append(columns)
            continue
        elif line.startswith("#"):
            continue
        elif line.endswith("\\"):
            current_line += line[:-1]
        else:
            current_line += line
            data_rows.append(current_line.split(separator))
            current_line = ""
    df = pd.DataFrame(data_rows, columns=columns)
    df.columns = df.columns.str.strip()
    return df


df_ssl = format_csv(PATH + 'ssl.log')
df_conn = format_csv(PATH + 'conn.log')
df_http = format_csv(PATH + 'http.log')
# df_x509 = format_csv('zeek_logs/x509.log')

merged_df = pd.merge(df_conn, df_ssl, on=["ts"], how="outer")
merged_df = pd.merge(merged_df, df_http, on=["ts"], how="outer")
# merged_df = pd.merge(merged_df, df_x509, on=["ts"], how="outer")
merged_df = merged_df.map(lambda x: x.strip() if isinstance(x, str) else x)


# merge infor handle
merged_df = merged_df[1: -1]
columns_to_drop = [col for col in merged_df.columns if col.endswith('_y')]

# x,y handle
merged_df = merged_df.drop(columns=columns_to_drop)
merged_df = merged_df.rename(columns=lambda x: x.rstrip('_x'))

merged_df.to_csv('dataset.csv', index=False)
print(merged_df.columns)
