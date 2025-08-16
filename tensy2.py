import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.model_split import train_test_split

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

# Generate amplitude list
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
    num = 90 * n + k
    n_norm = n / n_max
    k_onehot = [1 if i == coprime_90.index(k) else 0 for i in range(24)]
    dr = sum(int(d) for d in str(num)) % 9 or 9
    dr_onehot = [1 if dr == i else 0 for i in [1, 2, 4, 5, 7, 8]]
    ld = num % 10
    ld_onehot = [1 if ld == i else 0 for i in [1, 3, 7, 9]]
    features = k_onehot + [n_norm] + dr_onehot + ld_onehot  # 35 features
    label = 1 if amplitude_list[n] >= 1 else 0
    data.append(features + [label])

data = np.array(data)
X = data[:, :-1]  # 35 features
y = data[:, -1]

# Split data
X_train_full, X_test, y_train_full, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
X_train, X_val, y_train, y_val = train_test_split(X_train_full, y_train_full, test_size=0.2, random_state=42)

# Class weights (corrected for Keras)
total = len(y)
primes = sum(y == 0)
composites = sum(y == 1)
class_weight = {0: total / (2 * primes), 1: total / (2 * composites)}  # ~1.475, ~0.756
print(f"Class weights: {class_weight}")

# Build model
model = Sequential([
    Dense(128, activation='relu', input_dim=35),
    Dense(64, activation='relu'),
    Dense(32, activation='relu'),
    Dense(1, activation='sigmoid')
])
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train model
history = model.fit(X_train, y_train, epochs=100, batch_size=32, 
                    validation_data=(X_val, y_val), class_weight=class_weight, verbose=1)

# Evaluate model
loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
print(f"Test Accuracy: {accuracy * 100:.2f}%")

# Predict and verify
predictions = (model.predict(X_test) >= 0.5).astype(int).flatten()
primes_pred = sum(1 for pred in predictions if pred == 0)
composites_pred = sum(1 for pred in predictions if pred == 1)
primes_true = sum(1 for label in y_test if label == 0)
composites_true = sum(1 for label in y_test if label == 1)
print(f"Predicted Primes: {primes_pred}, True Primes: {primes_true}")
print(f"Predicted Composites: {composites_pred}, True Composites: {composites_true}")

# Derive address list
X_full = data[:, :-1]
y_pred_full = (model.predict(X_full) >= 0.5).astype(int)
address_list_pred = [90 * n + k for n in range(n_max + 1) if y_pred_full[n] == 0]
address_list_true = [90 * n + k for n in range(n_max + 1) if amplitude_list[n] == 0]
print(f"\nPredicted Prime Addresses (first 10): {address_list_pred[:10]}")
print(f"True Prime Addresses (first 10): {address_list_true[:10]}")
print(f"Total Predicted Primes: {len(address_list_pred)}, Total True Primes: {len(address_list_true)}")

# Sample predictions
print("\nSample Predictions:")
for i in range(min(10, len(X_test))):
    n_test = int(X_test[i, 24] * n_max)
    num = 90 * n_test + k
    pred = predictions[i]
    true = y_test[i]
    print(f"n={n_test}, Num={num}, Predicted: {'Composite' if pred else 'Prime'}, True: {'Composite' if true else 'Prime'}")