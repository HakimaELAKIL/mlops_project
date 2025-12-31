import argparse
import os
import pickle
import time
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score

# ---------------------- ARGUMENTS -------------------------
parser = argparse.ArgumentParser()
parser.add_argument("--layers", type=int, default=1)
parser.add_argument("--units", type=int, default=32)
parser.add_argument("--activation", type=str, default="relu")
parser.add_argument("--lr", type=float, default=0.01)
parser.add_argument("--export_path", type=str, required=True)
args = parser.parse_args()

# ---------------------- DATA -------------------------
data = load_iris()
X, y = data.data, data.target
sc = StandardScaler()
X = sc.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ---------------------- MODEL -------------------------
hidden_layers = tuple([args.units] * args.layers)
model_path = os.path.join(args.export_path, "model.pkl")

# Load previous model if exists
if os.path.exists(model_path):
    with open(model_path, "rb") as f:
        model = pickle.load(f)
else:
    model = MLPClassifier(
        hidden_layer_sizes=hidden_layers,
        activation=args.activation,
        learning_rate_init=args.lr,
        max_iter=1,        # one epoch at a time
        warm_start=True,   # continuous training
        random_state=42
    )

# ---------------------- TRAINING WITH EARLY STOPPING -------------------------
best_acc = 0
patience = 5
wait = 0
epochs = 50

for epoch in range(epochs):
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    print(f"accuracy={acc}")  # Katib reads this metric

    # Early stopping
    if acc > best_acc:
        best_acc = acc
        wait = 0
    else:
        wait += 1

    if wait >= patience:
        print(f"Early stopping at epoch {epoch+1}")
        break

# ---------------------- EXPORT MODEL -------------------------
os.makedirs(args.export_path, exist_ok=True)
with open(model_path, "wb") as f:
    pickle.dump(model, f)
print(f"Model exported to {args.export_path}")

time.sleep(5)

