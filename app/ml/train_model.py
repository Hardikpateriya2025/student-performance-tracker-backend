"""
Trains two models on the synthetic student dataset:
1. RandomForestRegressor -> predicts next_score (continuous)
2. RandomForestClassifier -> predicts at_risk (0/1)

Saves both trained models + feature list to app/ml/models/
Run this after generate_synthetic_data.py
"""
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import mean_absolute_error, r2_score, accuracy_score, classification_report

FEATURES = ["past_avg_score", "attendance_percent", "score_trend", "study_hours_per_week"]

def main():
    df = pd.read_csv("app/ml/data/synthetic_students.csv")

    X = df[FEATURES]
    y_reg = df["next_score"]
    y_clf = df["at_risk"]

    # Split once, reuse the same split for both models for consistency
    X_train, X_test, y_reg_train, y_reg_test, y_clf_train, y_clf_test = train_test_split(
        X, y_reg, y_clf, test_size=0.2, random_state=42
    )

    # --- Regression model: predict next score ---
    reg_model = RandomForestRegressor(n_estimators=200, max_depth=8, random_state=42)
    reg_model.fit(X_train, y_reg_train)
    reg_preds = reg_model.predict(X_test)

    mae = mean_absolute_error(y_reg_test, reg_preds)
    r2 = r2_score(y_reg_test, reg_preds)

    print("=== Regression Model (Next Score Prediction) ===")
    print(f"Mean Absolute Error: {mae:.2f} points")
    print(f"R² Score: {r2:.3f}")

    # --- Classification model: predict at-risk ---
    clf_model = RandomForestClassifier(n_estimators=200, max_depth=8, random_state=42)
    clf_model.fit(X_train, y_clf_train)
    clf_preds = clf_model.predict(X_test)

    acc = accuracy_score(y_clf_test, clf_preds)

    print("\n=== Classification Model (At-Risk Prediction) ===")
    print(f"Accuracy: {acc:.3f}")
    print(classification_report(y_clf_test, clf_preds, target_names=["Not At-Risk", "At-Risk"]))

    # --- Feature importance (which factors matter most) ---
    print("\n=== Feature Importance (Regression) ===")
    for feat, imp in sorted(zip(FEATURES, reg_model.feature_importances_), key=lambda x: -x[1]):
        print(f"{feat}: {imp:.3f}")

    # --- Save models ---
    joblib.dump(reg_model, "app/ml/models/score_regressor.joblib")
    joblib.dump(clf_model, "app/ml/models/risk_classifier.joblib")
    joblib.dump(FEATURES, "app/ml/models/features.joblib")

    print("\n✅ Models saved to app/ml/models/")


if __name__ == "__main__":
    main()
