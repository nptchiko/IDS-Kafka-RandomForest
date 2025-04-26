# not done yet - copy from chat
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib

# Load historical Zeek logs (e.g., conn.log in JSON format)
data = pd.read_json('historical_conn.log', lines=True)

# Select features
features = ['duration', 'orig_bytes', 'resp_bytes',
            'orig_pkts', 'resp_pkts', 'service', 'conn_state']
X = data[features]
y = data['label']  # Assume 'label' is 0 (benign) or 1 (malicious)

# Preprocess: Handle missing values
X = X.fillna({'duration': 0, 'orig_bytes': 0, 'resp_bytes': 0, 'orig_pkts': 0,
             'resp_pkts': 0, 'service': 'unknown', 'conn_state': 'unknown'})

# Encode categorical variables
label_encoders = {}
for col in ['service', 'conn_state']:
    label_encoders[col] = LabelEncoder()
    X[col] = label_encoders[col].fit_transform(X[col])

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# Train Random Forest
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save the model
joblib.dump(model, 'random_forest_model.pkl')

# Save label encoders for later use
for col, encoder in label_encoders.items():
    joblib.dump(encoder, f'label_encoder_{col}.pkl')
