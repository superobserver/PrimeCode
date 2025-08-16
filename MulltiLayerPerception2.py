import numpy as np
import sklearn
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Print scikit-learn version
print(f"scikit-learn version: {sklearn.__version__}")

# Define operators for k=11
operators = [
    (7, 53, 120, 34), (19, 29, 132, 48), (17, 43, 120, 38), (13, 77, 90, 11),
    (11, 91, 78, -1), (31, 41, 108, 32), (23, 67, 90, 17), (49, 59, 72, 14),
    (37, 83, 60, 4), (47, 73, 60, 8), (61, 71, 48, 6), (79, 89, 12, 0)
]

# Constants
n_max = 2191
k = 11
coprime_90 = [7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 49, 53, 59, 61, 67, 71, 73, 77, 79, 83, 89, 91]

# Generate amplitude list (sieve output)
amplitude_list = [0] * (n_max + 1)
for p, q, l, m in operators:
    x = 1
    while True:
        y = 90 * (x * x) - l * x + m
        if y > n_max:
            break
        p_x = p + 90 * (x - 1)
        q_x = q + 90 * (x - 1)
        if 0 <= y <= n_max:
            amplitude_list[y] += 1
        for t in range(1, int((n_max - y) / p_x) + 1):
            n = y + p_x * t
            if 0 <= n <= n_max:
                amplitude_list[n] += 1
        for t in range(1, int((n_max - y) / q_x) + 1):
            n = y + q_x * t
            if 0 <= n <= n_max:
                amplitude_list[n] += 1
        x += 1

# Prepare data
data = []
for n in range(n_max + 1):
    n_norm = n / n_max
    k_onehot = [1 if i == coprime_90.index(k) else 0 for i in range(24)]
    features = k_onehot + [n_norm]
    label = 1 if amplitude_list[n] >= 1 else 0  # Symmetry (1) vs. Anti-symmetry (0)
    data.append(features + [label])

data = np.array(data)
X = data[:, :-1]  # Features: k (24), n_norm (1) = 25
y = data[:, -1]   # Labels from amplitude list

# Split data
X_train_full, X_test, y_train_full, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
X_train, X_val, y_train, y_val = train_test_split(X_train_full, y_train_full, test_size=0.2, random_state=42)

# Class weight (optional, based on version)
class_weight = {0: len(y) / (2 * sum(y == 0)), 1: len(y) / (2 * sum(y == 1))}
print(f"Class weights: {class_weight}")

# Build and train model
try:
    # With class_weight (for scikit-learn >= 0.18)
    model = MLPClassifier(hidden_layer_sizes=(128, 64), activation='relu', solver='adam', 
                          learning_rate_init=0.005, max_iter=2000, tol=1e-5, 
                          random_state=42, verbose=True, class_weight=class_weight)
except TypeError:
    print("Warning: 'class_weight' not supported in this scikit-learn version. Proceeding without it.")
    # Without class_weight (fallback)
    model = MLPClassifier(hidden_layer_sizes=(128, 64), activation='relu', solver='adam', 
                          learning_rate_init=0.005, max_iter=2000, tol=1e-5, 
                          random_state=42, verbose=True)

model.fit(X_train, y_train)

# Monitor progress
print("\nTraining Progress:")
for i, loss in enumerate(model.loss_curve_):
    train_acc = accuracy_score(y_train, model.predict(X_train))
    val_acc = accuracy_score(y_val, model.predict(X_val))
    print(f"Iteration {i+1}, Loss = {loss:.8f}, Train Acc = {train_acc:.4f}, Val Acc = {val_acc:.4f}")

# Evaluate model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"\nTest Accuracy: {accuracy * 100:.2f}%")

# Verify counts
primes_pred = sum(1 for pred in y_pred if pred == 0)
composites_pred = sum(1 for pred in y_pred if pred == 1)
primes_true = sum(1 for label in y_test if label == 0)
composites_true = sum(1 for label in y_test if label == 1)
print(f"Predicted Primes: {primes_pred}, True Primes: {primes_true}")
print(f"Predicted Composites: {composites_pred}, True Composites: {composites_true}")

# Derive address list (anti-symmetry set)
address_list_pred = [90 * n + k for n in range(n_max + 1) if model.predict([X[n]])[0] == 0]
address_list_true = [90 * n + k for n in range(n_max + 1) if amplitude_list[n] == 0]
print(f"\nPredicted Prime Addresses (first 10): {address_list_pred[:10]}")
print(f"True Prime Addresses (first 10): {address_list_true[:10]}")
print(f"Total Predicted Primes: {len(address_list_pred)}, Total True Primes: {len(address_list_true)}")

# Sample predictions
print("\nSample Predictions:")
for i in range(min(10, len(X_test))):
    n_test = int(X_test[i, 24] * n_max)
    num = 90 * n_test + k
    pred = y_pred[i]
    true = y_test[i]
    print(f"n={n_test}, Num={num}, Predicted: {'Composite' if pred else 'Prime'}, True: {'Composite' if true else 'Prime'}")