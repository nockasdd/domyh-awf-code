---
name: ml-pipelines
description: "Machine learning pipeline patterns. Use when building ML training, evaluation, or deployment workflows."
detect: ["dvc.yaml", "mlflow", "Artifacts/", "Notebook_Experiments/", "scores.json"]
category: ai-ml
tier: 2
---

# ML Pipeline Patterns — DOMYH Awesome Code

> **Scope**: End-to-end ML projects with scikit-learn, TensorFlow, PyTorch
> **MLOps**: DVC, MLflow, DagsHub, GitHub Actions
> **Serving**: Flask, FastAPI, Streamlit, Docker

---

## 🎯 When to Use This Skill

Use for: ML model development, data science projects, MLOps pipelines.
**NOT for**: LLM/GenAI apps (→ ai-agents, rag-patterns), pure data analysis (→ python).

---

## 📁 Standard Project Structure

```
{ProjectName}/
├── src/{ProjectName}/
│   ├── __init__.py
│   ├── components/
│   │   ├── __init__.py
│   │   ├── data_ingestion.py      # Load raw data
│   │   ├── data_transformation.py  # Feature engineering
│   │   ├── model_trainer.py        # Train & compare models
│   │   └── model_evaluation.py     # Metrics & validation
│   ├── pipelines/
│   │   ├── __init__.py
│   │   ├── training_pipeline.py    # Orchestrate training
│   │   └── prediction_pipeline.py  # Load model & predict
│   ├── config/
│   │   └── configuration.py        # Paths, params
│   ├── utils/
│   │   └── common.py               # Logging, helpers
│   └── exception.py                # Custom exceptions
├── Artifacts/                       # Models, preprocessors, data
├── Notebook_Experiments/            # EDA & prototyping
├── static/                          # Web UI assets
├── templates/                       # Jinja2 HTML templates
├── .github/workflows/               # CI/CD
├── .dvc/                            # DVC config
├── app.py                           # Flask/FastAPI/Streamlit app
├── template.py                      # Project scaffold generator
├── setup.py                         # Package config
├── requirements.txt
├── Dockerfile
├── dvc.yaml                         # DVC pipeline stages
├── dvc.lock                         # DVC lock file
└── README.md
```

---

## 🔄 Pipeline Flow

```
Data Source → data_ingestion.py → raw data (Artifacts/)
    ↓
data_transformation.py → preprocessor.pkl + train/test splits
    ↓
model_trainer.py → model.pkl (best of N algorithms)
    ↓
model_evaluation.py → scores.json + MLflow logging
    ↓
prediction_pipeline.py → app.py (Flask/Streamlit)
```

---

## 🧱 Core Components

### Data Ingestion

```python
# src/{Name}/components/data_ingestion.py
import pandas as pd
from dataclasses import dataclass
from sklearn.model_selection import train_test_split

@dataclass
class DataIngestionConfig:
    raw_data_path: str = "Artifacts/raw.csv"
    train_data_path: str = "Artifacts/train.csv"
    test_data_path: str = "Artifacts/test.csv"

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def initiate(self) -> tuple[str, str]:
        df = pd.read_csv("data/source.csv")
        df.to_csv(self.config.raw_data_path, index=False)

        train, test = train_test_split(df, test_size=0.2, random_state=42)
        train.to_csv(self.config.train_data_path, index=False)
        test.to_csv(self.config.test_data_path, index=False)

        return self.config.train_data_path, self.config.test_data_path
```

### Data Transformation

```python
# src/{Name}/components/data_transformation.py
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer

class DataTransformation:
    def get_transformer(self, num_cols: list, cat_cols: list) -> ColumnTransformer:
        num_pipeline = Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ])
        cat_pipeline = Pipeline([
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore")),
        ])
        return ColumnTransformer([
            ("num", num_pipeline, num_cols),
            ("cat", cat_pipeline, cat_cols),
        ])
```

### Model Trainer (Multi-Algorithm Comparison)

```python
# src/{Name}/components/model_trainer.py
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import pickle

class ModelTrainer:
    MODELS = {
        "LinearRegression": LinearRegression(),
        "RandomForest": RandomForestRegressor(n_estimators=100),
        "GradientBoosting": GradientBoostingRegressor(n_estimators=100),
    }

    def train(self, X_train, y_train, X_test, y_test) -> tuple[str, float]:
        best_score, best_name = -1, ""
        for name, model in self.MODELS.items():
            model.fit(X_train, y_train)
            score = r2_score(y_test, model.predict(X_test))
            if score > best_score:
                best_score, best_name = score, name

        best_model = self.MODELS[best_name]
        with open("Artifacts/model.pkl", "wb") as f:
            pickle.dump(best_model, f)
        return best_name, best_score
```

---

## 🚀 MLOps

### DVC Pipeline (`dvc.yaml`)

```yaml
stages:
  data_ingestion:
    cmd: python src/pipeline/stage_01_data_ingestion.py
    deps:
      - src/pipeline/stage_01_data_ingestion.py
    outs:
      - Artifacts/raw.csv
  
  data_transformation:
    cmd: python src/pipeline/stage_02_data_transformation.py
    deps:
      - src/pipeline/stage_02_data_transformation.py
      - Artifacts/raw.csv
    outs:
      - Artifacts/preprocessor.pkl

  model_trainer:
    cmd: python src/pipeline/stage_03_model_trainer.py
    deps:
      - Artifacts/preprocessor.pkl
    outs:
      - Artifacts/model.pkl
    metrics:
      - scores.json:
          cache: false
```

### MLflow Tracking

```python
import mlflow
import os

os.environ["MLFLOW_TRACKING_URI"] = "https://dagshub.com/user/repo.mlflow"

with mlflow.start_run():
    mlflow.log_param("model", best_name)
    mlflow.log_metric("r2_score", best_score)
    mlflow.sklearn.log_model(best_model, "model")
```

---

## 🐳 Deployment

### Flask App (`app.py`)

```python
from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)
model = pickle.load(open("Artifacts/model.pkl", "rb"))
preprocessor = pickle.load(open("Artifacts/preprocessor.pkl", "rb"))

@app.route("/predict", methods=["POST"])
def predict():
    features = np.array([[
        float(request.form[f]) for f in FEATURE_NAMES
    ]])
    transformed = preprocessor.transform(features)
    prediction = model.predict(transformed)[0]
    return render_template("result.html", prediction=prediction)
```

### Dockerfile

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

---

## ✅ ML Project Checklist

- [ ] EDA complete in `Notebook_Experiments/`
- [ ] Data pipeline: ingestion → transformation
- [ ] Multiple models compared
- [ ] Best model saved to `Artifacts/`
- [ ] MLflow tracking configured
- [ ] DVC data versioning setup
- [ ] Flask/Streamlit app created
- [ ] Dockerfile ready
- [ ] CI/CD pipeline configured
- [ ] README with setup instructions

---
