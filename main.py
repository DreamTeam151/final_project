import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
import joblib

# Загружаем модель ANN
model = load_model("ANN_model.keras")

# Загружаем scaler
scaler = joblib.load("scaler.pkl")

# Загружаем список признаков
feature_cols = joblib.load("features.pkl")

def preprocess_data(df, feature_cols):
    """
    Предобработка данных:
    - Обработка категориальных колонок
    - Кодирование one-hot
    - Добавление отсутствующих колонок
    - Приведение к набору признаков из обучения
    """
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()

    if 'total_charges' in df.columns:
        df['total_charges'] = pd.to_numeric(df['total_charges'], errors='coerce')

    if 'senior_citizen' in df.columns:
        df['senior_citizen'] = df['senior_citizen'].astype(str)

    df[categorical_cols] = df[categorical_cols].fillna('No')
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    df[num_cols] = df[num_cols].fillna(0)

    df_encoded = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

    for col in feature_cols:
        if col not in df_encoded.columns:
            df_encoded[col] = 0

    df_encoded = df_encoded[feature_cols]

    return df_encoded

def predict(df):
    """
    Делает предсказание модели на новых данных.
    """
    df_processed = preprocess_data(df, feature_cols)
    X_scaled = scaler.transform(df_processed)

    predictions = model.predict(X_scaled)
    return predictions

if __name__ == "__main__":
    input_df = pd.read_csv("internet_service_churn.csv")

    preds = predict(input_df)
    threshold = 0.5
    churn_pred = (preds > threshold).astype(int)

    df_processed = preprocess_data(input_df, feature_cols)
    print("Пропуски после обработки:", df_processed.isna().sum())

    print("Предсказания модели (вероятности):")
    print(preds)
    print("Бинарные предсказания (0 — останется, 1 — уйдёт):")
    print(churn_pred)
