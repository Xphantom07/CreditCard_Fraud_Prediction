from __future__ import annotations

import pickle
from functools import lru_cache
from pathlib import Path

import pandas as pd
from flask import Flask, render_template, request
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "fraud_detection_model.pkl"
DATA_PATH = BASE_DIR / "credit_fraud.csv"

FEATURE_COLUMNS = [
    "age",
    "transaction_amount",
    "account_balance",
    "num_transactions_today",
    "is_foreign_transaction",
    "transaction_hour",
    "prev_fraud_flag",
    "merchant_distance_km",
    "merchant_risk_score",
]
TARGET_COLUMN = "is_fraud"


@lru_cache(maxsize=1)
def get_model():
    """Load a saved model if available, otherwise train a fresh one from the CSV data."""
    if MODEL_PATH.exists():
        try:
            with MODEL_PATH.open("rb") as handle:
                return pickle.load(handle)
        except Exception as exc:  # pragma: no cover - defensive fallback
            print(f"Unable to load saved model: {exc}")

    df = pd.read_csv(DATA_PATH)
    for column in FEATURE_COLUMNS + [TARGET_COLUMN]:
        if column == "age":
            df[column] = (
                df[column]
                .astype(str)
                .str.extract(r"(\d+(?:\.\d+)?)", expand=False)
                .astype(float)
            )
        else:
            df[column] = pd.to_numeric(df[column], errors="coerce")

    df = df.dropna(subset=FEATURE_COLUMNS + [TARGET_COLUMN])
    X = df[FEATURE_COLUMNS]
    y = df[TARGET_COLUMN].astype(int)

    X_train, _, y_train, _ = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=42,
        stratify=y,
    )

    pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
            (
                "classifier",
                LogisticRegression(
                    max_iter=2000,
                    class_weight="balanced",
                    random_state=42,
                ),
            ),
        ]
    )
    pipeline.fit(X_train, y_train)

    with MODEL_PATH.open("wb") as handle:
        pickle.dump(pipeline, handle)

    return pipeline


def validate_form(form_data: dict) -> dict[str, str]:
    """Perform server-side validation to keep the dashboard robust."""
    errors: dict[str, str] = {}

    try:
        age = float(form_data.get("age", ""))
        if not 18 <= age <= 100:
            errors["age"] = "Age must be between 18 and 100."
    except (TypeError, ValueError):
        errors["age"] = "Please enter a valid age."

    try:
        amount = float(form_data.get("transaction_amount", ""))
        if amount < 0:
            errors["transaction_amount"] = "Transaction amount cannot be negative."
    except (TypeError, ValueError):
        errors["transaction_amount"] = "Please enter a valid transaction amount."

    try:
        balance = float(form_data.get("account_balance", ""))
        if balance < 0:
            errors["account_balance"] = "Account balance cannot be negative."
    except (TypeError, ValueError):
        errors["account_balance"] = "Please enter a valid account balance."

    try:
        today_transactions = float(form_data.get("num_transactions_today", ""))
        if today_transactions < 0:
            errors["num_transactions_today"] = "Transactions today cannot be negative."
    except (TypeError, ValueError):
        errors["num_transactions_today"] = "Please enter a valid number of transactions."

    try:
        hour = float(form_data.get("transaction_hour", ""))
        if not 0 <= hour <= 23:
            errors["transaction_hour"] = "Transaction hour must be between 0 and 23."
    except (TypeError, ValueError):
        errors["transaction_hour"] = "Please enter a valid transaction hour."

    try:
        distance = float(form_data.get("merchant_distance_km", ""))
        if distance < 0:
            errors["merchant_distance_km"] = "Merchant distance cannot be negative."
    except (TypeError, ValueError):
        errors["merchant_distance_km"] = "Please enter a valid merchant distance."

    try:
        risk_score = float(form_data.get("merchant_risk_score", ""))
        if not 1 <= risk_score <= 15:
            errors["merchant_risk_score"] = "Merchant risk score must be between 1 and 15."
    except (TypeError, ValueError):
        errors["merchant_risk_score"] = "Please enter a valid merchant risk score."

    return errors


def build_prediction_context(form_data: dict) -> dict:
    """Build the prediction result payload and recommendation list."""
    model = get_model()
    payload = pd.DataFrame([form_data], columns=FEATURE_COLUMNS)
    payload = payload.astype(float)

    probability = float(model.predict_proba(payload)[0][1])
    prediction = int(probability >= 0.5)

    if prediction == 1:
        label = "Fraudulent Transaction"
        risk_level = "Critical Risk" if probability >= 0.85 else "High Risk" if probability >= 0.65 else "Medium Risk"
        recommendations = [
            "Verify customer identity before approval.",
            "Request OTP verification for the transaction.",
            "Hold the transaction temporarily for review.",
            "Notify the fraud monitoring team immediately.",
        ]
    else:
        label = "Legitimate Transaction"
        risk_level = "Low Risk" if probability <= 0.25 else "Medium Risk" if probability <= 0.5 else "Low Risk"
        recommendations = [
            "Transaction appears safe and consistent with profile.",
            "Continue processing without additional friction.",
            "Monitor for unusual patterns as a standard safeguard.",
        ]

    if probability >= 0.75:
        progress_color = "bg-red-500"
    elif probability >= 0.4:
        progress_color = "bg-amber-500"
    else:
        progress_color = "bg-emerald-500"

    return {
        "prediction": prediction,
        "prediction_label": label,
        "probability": probability,
        "risk_level": risk_level,
        "recommendations": recommendations,
        "progress_color": progress_color,
    }


@app.route("/", methods=["GET", "POST"])
def index():
    """Render the dashboard and handle prediction requests."""
    form_values = {}
    result = None
    validation_errors = {}

    if request.method == "POST":
        form_values = request.form.to_dict()
        validation_errors = validate_form(form_values)

        if not validation_errors:
            numeric_values = {}
            for field in FEATURE_COLUMNS:
                numeric_values[field] = float(form_values.get(field, 0))
            result = build_prediction_context(numeric_values)

    return render_template(
        "index.html",
        prediction=result["prediction"] if result else None,
        probability=result["probability"] if result else None,
        prediction_label=result["prediction_label"] if result else None,
        risk_level=result["risk_level"] if result else None,
        recommendations=result["recommendations"] if result else None,
        progress_color=result["progress_color"] if result else "bg-slate-300",
        validation_errors=validation_errors,
        form_values=form_values,
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
