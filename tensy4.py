import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.optimizers import Adam
from sklearn.model_split import train_test_split

# Constants
n_max = 2191
k = 11

# Single operator for k=11: (7, 53, 120, 34)
operator = (7, 53, 120, 34)
p, q, l, m = operator

# Generate amplitude list for p=7
amplitude_p = [0] * (n_max + 1)
insertion_points_p = set()
x = 1
while True:
    y = 90 * (x * x) - l * x + m
    if y > n_max:
        break
    p_x = p + 90 * (x - 1)
    if 0 <= y <= n_max:
        amplitude_p[y] += 1
        insertion_points_p.add(y)
    for t in range(1, int((n_max - y) / p_x) + 1):
        n = y + p_x * t
        if 0 <= n <= n_max:
            amplitude_p[n] += 1
    x += 1

# Generate amplitude list for q=53
amplitude_q = [0] * (n_max + 1)
insertion_points_q = set()
x = 1
while True:
    y = 90 * (x * x) - l * x + m
    if y > n_max:
        break
    q_x = q + 90 * (x - 1)
    if 0 <= y <= n_max:
        amplitude_q[y] += 1
        insertion_points_q.add(y)
    for t in range(1, int((n_max - y) / q_x) + 1):
        n = y + q_x * t
        if 0 <= n <= n_max:
            amplitude_q[n] += 1
    x += 1

# Prepare data for p=7
data_p = []
for n in range(n_max + 1):
    n_norm = n / n_max
    skew = min(abs(n - ip) for ip in insertion_points_p) / n_max if insertion_points_p else 0
    features = [n_norm, skew]
    label = 1 if amplitude_p[n] >= 1 else 0
    data_p.append(features + [label])

data_p = np.array(data_p)
X_p = data_p[:, :-1]
y_p = data_p[:, -1]

# Prepare data for q=53
data_q = []
for n in range(n_max + 1):
    n_norm = n / n_max
    skew = min(abs(n - ip) for ip in insertion_points_q) / n_max if insertion_points_q else 0
    features = [n_norm, skew]
    label = 1 if amplitude_q[n] >= 1 else 0
    data_q.append(features + [label])

data_q = np.array(data_q)
X_q = data_q[:, :-1]
y_q = data_q[:, -1]

# Split data for p=7
X_train_p_full, X_test_p, y_train_p_full, y_test_p = train_test_split(X_p, y_p, test_size=0.2, random_state=42)
X_train_p, X_val_p, y_train_p, y_val_p = train_test_split(X_train_p_full, y_train_p_full, test_size=0.2, random_state=42)

# Split data for q=53
X_train_q_full, X_test_q, y_train_q_full, y_test_q = train_test_split(X_q, y_q, test_size=0.2, random_state=42)
X_train_q, X_val_q, y_train_q, y_val_q = train_test_split(X_train_q_full, y_train_q_full, test_size=0.2, random_state=42)

# Class weights
class_weight_p = {0: len(y_p) / (2 * sum(y_p == 0)), 1: len(y_p) / (2 * sum(y_p == 1))}
class_weight_q = {0: len(y_q) / (2 * sum(y_q == 0)), 1: len(y_q) / (2 * sum(y_q == 1))}
print(f"Class weights for p=7: {class_weight_p}")
print(f"Class weights for q=53: {class_weight_q}")

# Model for p=7
model_p = Sequential([
    Dense(32, activation='relu', input_dim=2),
    Dense(16, activation='relu'),
    Dense(1, activation='sigmoid')
])
model_p.compile(loss='binary_crossentropy', optimizer=Adam(learning_rate=0.01), metrics=['accuracy'])
early_stopping = EarlyStopping(monitor='val_loss', patience=20, restore_best_weights=True)
history_p = model_p.fit(X_train_p, y_train_p, epochs=200, batch_size=32, 
                        validation_data=(X_val_p, y_val_p), class_weight=class_weight_p, 
                        callbacks=[early_stopping], verbose=1)

# Model for q=53
model_q = Sequential([
    Dense(32, activation='relu', input_dim=2),
    Dense(16, activation='relu'),
    Dense(1, activation='sigmoid')
])
model_q.compile(loss='binary_crossentropy', optimizer=Adam(learning_rate=0.01), metrics=['accuracy'])
history_q = model_q.fit(X_train_q, y_train_q, epochs=200, batch_size=32, 
                        validation_data=(X_val_q, y_val_q), class_weight=class_weight_q, 
                        callbacks=[early_stopping], verbose=1)

# Evaluate p=7
loss_p, accuracy_p = model_p.evaluate(X_test_p, y_test_p, verbose=0)
print(f"\nTest Accuracy for p=7: {accuracy_p * 100:.2f}%")
predictions_p = (model_p.predict(X_test_p) >= 0.5).astype(int).flatten()
hits_p = sum(predictions_p)
print(f"Predicted Hits for p=7: {hits_p}, Total Test Samples: {len(y_test_p)}")

# Evaluate q=53
loss_q, accuracy_q = model_q.evaluate(X_test_q, y_test_q, verbose=0)
print(f"Test Accuracy for q=53: {accuracy_q * 100:.2f}%")
predictions_q = (model_q.predict(X_test_q) >= 0.5).astype(int).flatten()
hits_q = sum(predictions_q)
print(f"Predicted Hits for q=53: {hits_q}, Total Test Samples: {len(y_test_q)}")

# Full address lists
y_pred_full_p = (model_p.predict(X_p) >= 0.5).astype(int)
addresses_p = [90 * n + k for n in range(n_max + 1) if y_pred_full_p[n] == 1]
y_pred_full_q = (model_q.predict(X_q) >= 0.5).astype(int)
addresses_q = [90 * n + k for n in range(n_max + 1) if y_pred_full_q[n] == 1]
print(f"\nPredicted Addresses for p=7 (first 10): {addresses_p[:10]}")
print(f"Predicted Addresses for q=53 (first 10): {addresses_q[:10]}")
print(f"Total Predicted Hits for p=7: {len(addresses_p)}")
print(f"Total Predicted Hits for q=53: {len(addresses_q)}")