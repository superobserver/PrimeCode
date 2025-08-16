import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import xgboost as xgb

# Step 1: Generate Ground Truth (k=11, n_max=2191)
n_max = 2191
A201804 = [0] * (n_max + 1)

def drLD(x, l, m, z, o, listvar):
    y = 90 * x * x - l * x + m
    if 0 <= y <= n_max:
        listvar[y] += 1
        p = z + 90 * (x - 1)
        q = o + 90 * (x - 1)
        for i in range(1, int((n_max - y) / p) + 1):
            if y + i * p <= n_max:
                listvar[y + i * p] += 1
        for i in range(1, int((n_max - y) / q) + 1):
            if y + i * q <= n_max:
                listvar[y + i * q] += 1

operators = [
    (72, -1, 17, 91), (108, 29, 19, 53), (72, 11, 37, 71), (18, 0, 73, 89),
    (102, 20, 11, 67), (138, 52, 13, 29), (102, 28, 31, 47), (48, 3, 49, 83),
    (78, 8, 23, 79), (132, 45, 7, 41), (78, 16, 43, 59), (42, 4, 61, 77)
]

for x in range(1, int(np.sqrt(n_max / 90)) + 2):
    for l, m, p, q in operators:
        drLD(x, l, m, p, q, A201804)

holes = [n for n in range(n_max + 1) if A201804[n] == 0]
composites = [n for n in range(n_max + 1) if A201804[n] >= 1]
print(f"Number of holes (primes): {len(holes)}")
print(f"First 10 holes: {holes[:10]}")
print(f"Last 10 holes: {holes[-10:]}")
print(f"Number of composites: {len(composites)}")

# Step 2: Amplitude Feature
X = np.array([[A201804[n]] for n in range(n_max + 1)])
y = np.array([1 if n in composites else 0 for n in range(n_max + 1)])  # 1 for composite, 0 for hole

# Step 3: Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 4: Train XGBoost
model = xgb.XGBClassifier(
    n_estimators=100,
    max_depth=5,
    learning_rate=0.01,
    random_state=42
)
model.fit(X_train, y_train)

# Step 5: Evaluate ML Prediction
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Test Accuracy (composites, ML): {accuracy * 100:.2f}%")
print("Classification Report (0=hole, 1=composite):")
print(classification_report(y_test, y_pred, target_names=['Hole', 'Composite']))

# Step 6: Predict Composites and Infer Holes (ML)
predictions = model.predict(X)
predicted_composites = [n for n in range(n_max + 1) if predictions[n] == 1]
predicted_holes = [n for n in range(n_max + 1) if predictions[n] == 0]
print(f"Number of predicted composites (ML): {len(predicted_composites)}")
print(f"Number of predicted holes (ML): {len(predicted_holes)}")
print(f"First 10 predicted holes (ML): {predicted_holes[:10]}")
print(f"Last 10 predicted holes (ML): {predicted_holes[-10:]}")
print(f"Accuracy of hole prediction (ML): {sum(1 for n in holes if n in predicted_holes) / len(holes) * 100:.2f}%")

# Step 7: Deterministic Prediction
det_predicted_holes = [n for n in range(n_max + 1) if A201804[n] == 0]
print(f"\nNumber of predicted holes (Deterministic): {len(det_predicted_holes)}")
print(f"First 10 predicted holes (Deterministic): {det_predicted_holes[:10]}")
print(f"Last 10 predicted holes (Deterministic): {det_predicted_holes[-10:]}")
print(f"Accuracy of hole prediction (Deterministic): {sum(1 for n in holes if n in det_predicted_holes) / len(holes) * 100:.2f}%")

# Diagnostics
ml_false_negatives = [n for n in holes if n not in predicted_holes]
ml_false_positives = [n for n in predicted_holes if n not in holes]
print(f"ML False Negatives (missed holes): {len(ml_false_negatives)}")
print(f"ML False Positives (extra predicted holes): {len(ml_false_positives)}")