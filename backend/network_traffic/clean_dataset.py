import pandas as pd
import numpy as np
from datetime import datetime


# df = pd.read_json('../../data/logs/merged.log', lines=True)

# feature = ['proto', 'service', 'id.resp_p', 'missed_bytes', 'version', 'cipher', 'curve',
#     'resumed','established', 'sni_matches_cert']

# df = df[feature]
# df.replace(["", "-", "NULL"], pd.NA, inplace=True)
# df['id.resp_p'] = pd.to_numeric(df['id.resp_p'], errors='coerce').astype('Int64')
# df['missed_bytes'] = pd.to_numeric(df['missed_bytes'], errors='coerce').astype('Int64')

# # df['username'] = np.where(
# #     df['username'].notna(),
# #     0,
# #     1
# # )

# # df['password'] = np.where(
# #     df['password'].notna(),
# #     0,
# #     1
# # )

# df['version'] = np.where(
#     df['version'].notna() & ~df['version'].isin(['TLSv1.2', 'TLSv1.3']),
#     0,
#     1
# )
# df['cipher'] = np.where(
#     df['cipher'].notna() &
#     df['cipher'].str.contains('AES', na=False).eq(False) &
#     df['cipher'].str.contains('GCM', na=False).eq(False) &
#     df['cipher'].str.contains('ChaCha20', na=False).eq(False),
#     0,
#     1
# )


# df['curve'] = np.where(
#     df['curve'].notna() & df['curve'].isin(['secp256r1', 'secp384r1', 'secp521r1', 'x25519']),
#     0,
#     1
# )

# df['resumed'] = np.where(
#     df['resumed'].notna() & df['resumed'] == 'T',
#     0,
#     1
# )

# df['established'] = np.where(
#     df['established'].notna() & df['established'] == 'F',
#     0,
#     1
# )

# df['sni_matches_cert'] = np.where(
#     df['sni_matches_cert'].notna() & df['sni_matches_cert'] == 'F',
#     0,
#     1
# )

# df['secure_label'] = np.where(
#     ((df['service'] == 'dns') & (df['id.resp_p'] == 53)) |
#     ((df['service'] == 'dhcp') & ((df['id.resp_p'] == 67) | (df['id.resp_p'] == 68))) |
#     ((df['service'] == 'ntp') & (df['id.resp_p'] == 123)) |
#     (df['proto'] == 'unknown_transport')|
#     (df['missed_bytes'].notna() & (df['missed_bytes'] > 0)) |
#     # (df['username'] == 0) |
#     # (df['password'] == 0) |
#     (df['version'] == 0) |
#     (df['cipher'] == 0) |
#     (df['curve'] == 0) |
#     (df['resumed'] == 0) |
#     (df['established'] == 0) |
#     (df['sni_matches_cert'] == 0),

#     0,  # Value if condition is True (insecure)
#     1   # Value if condition is False (secure)
# )

df = pd.read_csv('clean_dataset.csv')

# df.to_csv('clean_dataset.csv')
print(df['secure_label'].value_counts())
