import pandas as pd
import numpy as np
from datetime import datetime


df = pd.read_csv('/data/logs/merged.log', dtype=str, low_memory=False)
# feature = ['proto', 'service', 'id.resp_p', 'missed_bytes', 'version', 'cipher', 'curve',
#     'resumed', 'last_alert', 'established', 'sni_matches_cert', 'username', 'password',
#     'certificate.not_valid_before', 'certificate.not_valid_after', 'certificate.key_alg',
#     'certificate.sig_alg', 'certificate.key_length']

feature = ['proto', 'service', 'id.resp_p', 'missed_bytes', 'version', 'cipher', 'curve',
    'resumed', 'last_alert', 'established', 'sni_matches_cert', 'username', 'password']

df = df[feature]
df.replace(["", "-", "NULL"], pd.NA, inplace=True)
df['id.resp_p'] = pd.to_numeric(df['id.resp_p'], errors='coerce').astype('Int64')
# df['certificate.key_length'] = pd.to_numeric(df['certificate.key_length'], errors='coerce').astype('Int64')
# df['certificate.not_valid_after'] = pd.to_datetime(pd.to_numeric(df['certificate.not_valid_after'], errors='coerce'), unit='s')
# df['certificate.not_valid_before'] = pd.to_datetime(pd.to_numeric(df['certificate.not_valid_before'], errors='coerce'), unit='s')
df['missed_bytes'] = pd.to_numeric(df['missed_bytes'], errors='coerce').astype('Int64')

df['username'] = np.where(
    df['username'].notna(),
    0,
    1
)

df['password'] = np.where(
    df['password'].notna(),
    0,
    1
)

# df['certificate.not_valid_before'] = np.where(
#     df['certificate.not_valid_before'].notna() & (df['certificate.not_valid_before'] > datetime.now()),
#     0,
#     1
# )

# df['certificate.not_valid_after'] = np.where(
#     df['certificate.not_valid_after'].notna() & (df['certificate.not_valid_after'] < datetime.now()),
#     0,
#     1
# )

# df['certificate.key'] = np.where(
#     (df['certificate.key_alg'].notna() & df['certificate.key_alg'] == 'rsaEncryption') & (df['certificate.key_length'].notna() & (df['certificate.key_length'] < 2048)),
#     0,
#     1
# )

# df['certificate.sig_alg'] = np.where(
#     df['certificate.sig_alg'].notna() & df['certificate.sig_alg'].isin(['sha256WithRSAEncryption', 'sha384WithRSAEncryption', 'sha512WithRSAEncryption']),
#     0,
#     1
# )

df['version'] = np.where(
    df['version'].notna() & ~df['version'].isin(['TLSv1.2', 'TLSv1.3']),
    0,
    1
)
df['cipher'] = np.where(
    df['cipher'].notna() &
    df['cipher'].str.contains('AES', na=False).eq(False) &
    df['cipher'].str.contains('GCM', na=False).eq(False) &
    df['cipher'].str.contains('ChaCha20', na=False).eq(False),
    0,
    1
)


df['curve'] = np.where(
    df['curve'].notna() & df['curve'].isin(['secp256r1', 'secp384r1', 'secp521r1', 'x25519']),
    0,
    1
)

df['resumed'] = np.where(
    df['resumed'].notna() & df['resumed'] == 'T',
    0,
    1
)

df['established'] = np.where(
    df['established'].notna() & df['established'] == 'F',
    0,
    1
)

df['sni_matches_cert'] = np.where(
    df['sni_matches_cert'].notna() & df['sni_matches_cert'] == 'F',
    0,
    1
)

df['secure_label'] = np.where(
    ((df['service'] == 'dns') & (df['id.resp_p'] == 53)) |
    ((df['service'] == 'dhcp') & ((df['id.resp_p'] == 67) | (df['id.resp_p'] == 68))) |
    ((df['service'] == 'ntp') & (df['id.resp_p'] == 123)) |
    (df['proto'] == 'unknown_transport')|
    (df['missed_bytes'].notna() & (df['missed_bytes'] > 0)) |
    (df['username'] == 0) |
    (df['password'] == 0) |
    # (df['certificate.not_valid_before'] == 0) |
    # (df['certificate.not_valid_after'] == 0) |
    # (df['certificate.key'] == 0) |
    # (df['certificate.sig_alg'] == 0) |
    (df['version'] == 0) |
    (df['cipher'] == 0) |
    (df['curve'] == 0) |
    (df['resumed'] == 0) |
    (df['established'] == 0) |
    (df['sni_matches_cert'] == 0),

    0,  # Value if condition is True (insecure)
    1   # Value if condition is False (secure)
)

df.to_csv('clean_dataset.csv')
print(df['secure_label'].value_counts())
