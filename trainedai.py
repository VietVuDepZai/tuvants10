import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
import joblib

# Load data
with open('best.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Prepare features and labels
# Include address, district, scores (nv1, nv2, nv3), and isChuyen as features
X_text = [item['dia_chi'] + ' ' + item['quan_huyen'] for item in data]
X_numeric = [[item['nv1'], item['nv2'], item['nv3'], item['isChuyen']] for item in data]
y = [item['ten_truong'] for item in data]

# Vectorize the text-based features
vectorizer = CountVectorizer()
X_text_vectorized = vectorizer.fit_transform(X_text)

# Combine text and numeric features
import numpy as np
X_combined = np.hstack((X_text_vectorized.toarray(), X_numeric))

# Scale the numeric features to ensure they have similar influence as text features
scaler = StandardScaler()
X_combined_scaled = scaler.fit_transform(X_combined)

# Train the model
model = KNeighborsClassifier(n_neighbors=1)
model.fit(X_combined_scaled, y)

# Save the model, vectorizer, and scaler
joblib.dump(model, 'school_finder_model.pkl')
joblib.dump(vectorizer, 'vectorizer.pkl')
joblib.dump(scaler, 'scaler.pkl')
