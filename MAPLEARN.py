import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import xgboost as xgb

# Step 1: Generate Ground Truth with Sieve (k=11, n_max=2191)
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
    (120, 34, 7, 53), (132, 48, 19, 29), (120, 38, 17, 43), (90, 11, 13, 77),
    (78, -1, 11, 91), (108, 32, 31, 41), (90, 17, 23, 67), (72, 14, 49, 59),
    (60, 4, 37, 83), (60, 8, 47, 73), (48, 6, 61, 71), (12, 0, 79, 89)
]

for x in range(1, int(np.sqrt(n_max / 90)) + 2):
    for l, m, p, q in operators:
        drLD(x, l, m, p, q, A201804)

holes = [n for n in range(n_max + 1) if A201804[n] == 0]
print(f"Number of holes (primes): {len(holes)}")
print(f"First 10 holes: {holes[:10]}")
print(f"Last 10 holes: {holes[-10:]}")

# Step 2: Compute Features (Enhanced)
def compute_features(n, operators, amplitudes):
    digits = [int(d) for d in str(n).zfill(4)][:4]
    gaps = [digits[i+1] - digits[i] for i in range(3)] if n >= 10 else [0, 0, digits[-1]]
    dr = sum(digits) % 9 or 9
    ld = n % 10
    amplitude = amplitudes[n]  # Direct sieve output
    distances = []
    x_range = range(1, int(np.sqrt(n_max / 90)) + 2)  # Match sieve range
    for l, m, p, q in operators:
        quad_dists = [abs(n - (90 * x * x - l * x + m)) for x in x_range]
        min_quad_dist = min(quad_dists, default=n)
        # Include periodic distances (simplified approximation)
        periodic_dists = [abs(n - (90 * x * x - l * x + m + i * p)) for x in x_range for i in range(5)]
        min_periodic_p = min(periodic_dists, default=n)
        periodic_dists_q = [abs(n - (90 * x * x - l * x + m + i * q)) for x in x_range for i in range(5)]
        min_periodic_q = min(periodic_dists_q, default=n)
        distances.extend([min_quad_dist, min_periodic_p, min_periodic_q])
    return np.array(digits + gaps + [dr, ld, amplitude] + distances)

X = np.array([compute_features(n, operators, A201804) for n in range(n_max + 1)])
y = np.array([0 if n in holes else 1 for n in range(n_max + 1)])

# Step 3: Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 4: Build and Train XGBoost Classifier
model = xgb.XGBClassifier(
    n_estimators=200,
    max_depth=10,
    learning_rate=0.01,
    scale_pos_weight=len(y[y==1]) / len(y[y==0]),  # Balance classes
    random_state=42
)
model.fit(X_train, y_train)

# Step 5: Evaluate
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Test Accuracy: {accuracy * 100:.2f}%")
print("Classification Report:")
print(classification_report(y_test, y_pred, target_names=['Hole', 'Composite']))

# Step 6: Predict and Validate
predictions = model.predict(X)
predicted_holes = [n for n in range(n_max + 1) if predictions[n] == 0]
print(f"Number of predicted holes: {len(predicted_holes)}")
print(f"First 10 predicted holes: {predicted_holes[:10]}")
print(f"Last 10 predicted holes: {predicted_holes[-10:]}")
print(f"Accuracy of hole prediction: {sum(1 for n in holes if n in predicted_holes) / len(holes) * 100:.2f}%")

# Diagnostics
false_negatives = [n for n in holes if n not in predicted_holes]
false_positives = [n for n in predicted_holes if n not in holes]
print(f"False Negatives (missed holes): {len(false_negatives)}")
print(f"False Positives (extra predicted holes): {len(false_positives)}")