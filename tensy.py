import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.model_selection import train_test_split

# Define operators for k=11 (from Table 3.1)
operators = [
    (7, 53, 120, 34),  # (p, q, l, m) for n = 90x^2 - lx + m
    (19, 29, 132, 48),
    (17, 43, 120, 38),
    (13, 77, 90, 11),
    (11, 91, 78, -1),
    (31, 41, 108, 32),
    (23, 67, 90, 17),
    (49, 59, 72, 14),
    (37, 83, 60, 4),
    (47, 73, 60, 8),
    (61, 71, 48, 6),
    (79, 89, 12, 0)
]

# Constants
n_max = 2191
k = 11
coprime_90 = [7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 49, 53, 59, 61, 67, 71, 73, 77, 79, 83, 89, 91]

# Helper functions
def digital_root(num):
    while num > 9:
        num = sum(int(d) for d in str(num))
    return num

def compute_amplitude(n, k, operators, n_max):
    amplitude = 0
    num = 90 * n + k
    for p, q, l, m in operators:
        x = 1
        while True:
            y = 90 * (x * x) - l * x + m
            if y > n_max:
                break
            p_x = p + 90 * (x - 1)
            q_x = q + 90 * (x - 1)
            if y == n:
                amplitude += 1
            for t in range(1, int((n_max - y) / p_x) + 1):
                if y + p_x * t == n:
                    amplitude += 1
            for t in range(1, int((n_max - y) / q_x) + 1):
                if y + q_x * t == n:
                    amplitude += 1
            x += 1
    return amplitude

# Generate data
data = []
for n in range(n_max + 1):
    num = 90 * n + k
    dr = digital_root(num)
    ld = num % 10
    amplitude = compute_amplitude(n, k, operators, n_max)
    # One-hot encode k (24 classes)
    k_onehot = [1 if i == coprime_90.index(k) else 0 for i in range(24)]
    # One-hot encode DR (6 classes: 1, 2, 4, 5, 7, 8)
    dr_onehot = [1 if dr == i else 0 for i in [1, 2, 4, 5, 7, 8]]
    # One-hot encode LD (4 classes: 1, 3, 7, 9)
    ld_onehot = [1 if ld == i else 0 for i in [1, 3, 7, 9]]
    # Normalize n
    n_norm = n / n_max
    features = k_onehot + [n_norm] + dr_onehot + ld_onehot
    data.append(features + [1 if amplitude >= 1 else 0])  # Binary label: 1=composite, 0=prime

data = np.array(data)
X = data[:, :-1]  # Features (35)
y = data[:, -1]   # Labels

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Build model
model = Sequential([
    Dense(64, activation='relu', input_dim=35),
    Dense(32, activation='relu'),
    Dense(1, activation='sigmoid')
])
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train model
history = model.fit(X_train, y_train, epochs=10, batch_size=32, validation_split=0.2, verbose=1)

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

# Check specific examples
for i in range(min(10, len(X_test))):
    n_test = int(X_test[i, 24] * n_max)  # Denormalize n
    num = 90 * n_test + k
    pred = predictions[i]
    true = y_test[i]
    print(f"n={n_test}, Num={num}, Predicted: {'Composite' if pred else 'Prime'}, True: {'Composite' if true else 'Prime'}")