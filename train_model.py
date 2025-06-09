import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
import pickle

# Wczytaj dane
df = pd.read_csv("dane_rekomendacyjne_500.csv")

# Podziel dane
X = df.drop(columns=["Skuteczność planu", "Ocena użytkownika"])
y = df["Skuteczność planu"]

# Zakoduj dane
encoders = {}
for col in X.columns:
    if X[col].dtype == 'object':
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col])
        encoders[col] = le

# Zakoduj y
target_encoder = LabelEncoder()
y = target_encoder.fit_transform(y)
encoders["Skuteczność planu"] = target_encoder

# Trening modelu
model = LogisticRegression(max_iter=1000, multi_class="multinomial")
model.fit(X, y)

# Zapisz model i encodery
with open("model_rekomendacji.pkl", "wb") as f:
    pickle.dump(model, f)

with open("label_encoders.pkl", "wb") as f:
    pickle.dump(encoders, f)
