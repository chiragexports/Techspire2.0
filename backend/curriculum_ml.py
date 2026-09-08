# -*- coding: utf-8 -*-
"""
Curriculum definition for Machine Learning Engineering & MLOps in Production.
Comprehensive 10-module curriculum covering ML mathematical foundations, classical algorithms,
ensemble trees (XGBoost), feature pipelines, MLOps lifecycle, model registries, and production serving.
"""

ML_COURSE = {
    "title": "Machine Learning Engineering & MLOps in Production",
    "slug": "machine-learning-engineering-mlops-production",
    "description": "Build end-to-end production ML pipelines, train high-performance gradient boosted trees, automate tracking with MLflow, and deploy low-latency inference microservices.",
    "category": "ai-ml",
    "level": "intermediate",
    "duration_weeks": 11,
    "thumbnail_gradient": "from-amber-600 via-orange-700 to-red-900",
    "is_featured": True,
    "modules": [
        {
            "order": 1,
            "title": "Mathematical Foundations & Statistical Learning Theory",
            "description": "Matrix calculus, eigenvalues, multivariate probability distributions, and the Bias-Variance tradeoff.",
            "chapters": [
                {
                    "order": 1,
                    "title": "The Bias-Variance Tradeoff & Generalization Error",
                    "description": "Deconstruct total expected test error into irreducible noise, model bias, and parameter variance.",
                    "duration_minutes": 35,
                    "content": """# The Bias-Variance Tradeoff

Total expected Mean Squared Error decomposes into three fundamental components:
$$\\mathbb{E}\\left[(y - \\hat{f}(x))^2\\right] = \\text{Bias}\\left[\\hat{f}(x)\\right]^2 + \\text{Var}\\left[\\hat{f}(x)\\right] + \\sigma^2$$

- **Underfitting (High Bias)**: The model is overly simplistic to capture true underlying functional relationships (e.g. fitting linear model to quadratic data).
- **Overfitting (High Variance)**: The model memorizes training noise and fails to generalize to unseen distributions.
- **Irreducible Error ($\sigma^2$)**: Inherent stochastic noise in the measurement process.

## Key Takeaways
- Increasing model complexity reduces bias but increases variance; regularizers (L1/L2) introduce controlled bias to drastically lower variance."""
                }
            ]
        },
        {
            "order": 2,
            "title": "Supervised Learning: Regression & Classification",
            "description": "Ordinary Least Squares, Logistic Regression, Ridge/Lasso/ElasticNet, and Loss surface convergence.",
            "chapters": [
                {
                    "order": 1,
                    "title": "Regularized Linear Models (L1 vs L2)",
                    "description": "Compare Lasso L1 sparsity induction with Ridge L2 weight decay shrinkage.",
                    "duration_minutes": 45,
                    "content": """# Regularized Linear Models

```python
import numpy as np
from sklearn.linear_model import Ridge, Lasso, ElasticNet

# L1 Regularization (Lasso): forces non-essential coefficients to exact zero (Feature Selection)
# Loss = MSE + alpha * sum(|w|)
lasso = Lasso(alpha=0.1)

# L2 Regularization (Ridge): shrinks weights smoothly towards zero
# Loss = MSE + alpha * sum(w^2)
ridge = Ridge(alpha=1.0)

# ElasticNet: Convex combination of L1 and L2 penalties
elastic = ElasticNet(alpha=0.1, l1_ratio=0.5)
```

## Key Geometric Intuition
- The L1 norm constraint boundary is a diamond shape with sharp corners aligning on coordinate axes, driving weights to exact zeros.
- The L2 norm boundary is a hypersphere with smooth tangents, shrinking weights smoothly."""
                }
            ]
        },
        {
            "order": 3,
            "title": "Tree-Based Models & Gradient Boosted Ensembles",
            "description": "Decision Trees (CART, Gini/Entropy), Random Forests (Bagging), and Gradient Boosting (XGBoost, LightGBM).",
            "chapters": [
                {
                    "order": 1,
                    "title": "Gradient Boosted Decision Trees (XGBoost & LightGBM)",
                    "description": "Derive second-order Taylor expansion loss approximations and histogram binning splits.",
                    "duration_minutes": 50,
                    "content": """# Gradient Boosting & XGBoost

Gradient boosting fits new weak learners sequentially to predict the negative gradients (pseudo-residuals) of the loss function:
$$F_m(x) = F_{m-1}(x) + \\eta h_m(x)$$

```python
import xgboost as xgb
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

X, y = make_classification(n_samples=10000, n_features=20, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = xgb.XGBClassifier(
    n_estimators=300,
    learning_rate=0.05,
    max_depth=5,
    subsample=0.8,
    colsample_bytree=0.8,
    tree_method="hist",  # High-speed histogram binning
    early_stopping_rounds=20,
    eval_metric="logloss"
)

model.fit(
    X_train, y_train,
    eval_set=[(X_test, y_test)],
    verbose=False
)
```

## Key Takeaways
- Bagging (Random Forest) reduces variance through parallel independent voting.
- Boosting (XGBoost) reduces bias through sequential error correction."""
                }
            ]
        },
        {
            "order": 4,
            "title": "Unsupervised Learning & Dimensionality Reduction",
            "description": "K-Means++, DBSCAN density clustering, Principal Component Analysis (PCA), and UMAP embeddings.",
            "chapters": [
                {
                    "order": 1,
                    "title": "Principal Component Analysis (PCA) & Singular Value Decomposition",
                    "description": "Project high-dimensional feature spaces onto maximal variance orthogonal eigenvectors.",
                    "duration_minutes": 40,
                    "content": """# Principal Component Analysis (PCA)

PCA finds orthogonal linear combinations of features that maximize explained variance:
$$\mathbf{X}^T \mathbf{X} = \mathbf{V} \mathbf{\Lambda} \mathbf{V}^T$$

```python
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# Crucial Step: Scale features to zero mean and unit variance
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

pca = PCA(n_components=0.95)  # Retain 95% of total variance
X_reduced = pca.fit_transform(X_scaled)

print(f"Reduced from {X.shape[1]} to {X_reduced.shape[1]} components.")
```

## Key Takeaways
- Always standardize features prior to running PCA to prevent high-magnitude features from dominating variance calculations."""
                }
            ]
        },
        {
            "order": 5,
            "title": "Feature Engineering, Leakage Prevention & Data Drift",
            "description": "Target encoding, cyclic time embeddings, pipeline serialization, and Kolmogorov-Smirnov drift tests.",
            "chapters": [
                {
                    "order": 1,
                    "title": "Robust Scikit-Learn Pipelines & Leakage Prevention",
                    "description": "Encapsulate transformations to prevent data leakage between train and test splits.",
                    "duration_minutes": 45,
                    "content": """# Production ML Pipelines & Leakage Prevention

Data leakage occurs when information outside the training dataset is inadvertently used to create the model.

```python
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.ensemble import RandomForestClassifier

num_features = ['age', 'income', 'credit_score']
cat_features = ['occupation', 'country']

preprocessor = ColumnTransformer(
    transformers=[
        ('num', Pipeline([
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler())
        ]), num_features),
        ('cat', Pipeline([
            ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
            ('encoder', OneHotEncoder(handle_unknown='ignore'))
        ]), cat_features)
    ]
)

full_pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(n_estimators=100))
])

# Fit on training data ONLY
full_pipeline.fit(X_train, y_train)
```"""
                }
            ]
        },
        {
            "order": 6,
            "title": "Model Evaluation & Hyperparameter Tuning",
            "description": "ROC-AUC, Precision-Recall curves, Stratified K-Fold, Cost-sensitive loss, and Optuna Bayesian search.",
            "chapters": [
                {
                    "order": 1,
                    "title": "Bayesian Hyperparameter Optimization with Optuna",
                    "description": "Tune hyperparameters via Tree-structured Parzen Estimators (TPE) with pruning callbacks.",
                    "duration_minutes": 45,
                    "content": """# Optuna Bayesian Hyperparameter Optimization

```python
import optuna
from sklearn.metrics import roc_auc_score

def objective(trial):
    params = {
        'n_estimators': trial.suggest_int('n_estimators', 50, 500),
        'max_depth': trial.suggest_int('max_depth', 3, 10),
        'learning_rate': trial.suggest_float('learning_rate', 1e-3, 0.3, log=True),
        'subsample': trial.suggest_float('subsample', 0.5, 1.0),
    }
    
    clf = xgb.XGBClassifier(**params)
    clf.fit(X_train, y_train)
    
    preds = clf.predict_proba(X_val)[:, 1]
    return roc_auc_score(y_val, preds)

study = optuna.create_study(direction="maximize")
study.optimize(objective, n_trials=50)

print(f"Best Trial ROC-AUC: {study.best_value:.4f}")
print("Best Params:", study.best_params)
```"""
                }
            ]
        },
        {
            "order": 7,
            "title": "MLOps: Experiment Tracking & Model Registry",
            "description": "MLflow tracking server, artifact storage, metric curves, model versioning, and lifecycle stage transitions.",
            "chapters": [
                {
                    "order": 1,
                    "title": "MLflow Experiment Tracking & Model Staging",
                    "description": "Log hyperparameters, confusion matrices, model artifacts, and promote models to Production.",
                    "duration_minutes": 45,
                    "content": """# MLflow Tracking & Model Registry

```python
import mlflow
import mlflow.sklearn

mlflow.set_experiment("fraud_detection_production")

with mlflow.start_run(run_name="xgboost_bayesian_run_42"):
    # Log hyperparameters
    mlflow.log_params(study.best_params)
    
    # Train model
    model = xgb.XGBClassifier(**study.best_params)
    model.fit(X_train, y_train)
    
    # Evaluate & log metrics
    val_auc = roc_auc_score(y_val, model.predict_proba(X_val)[:, 1])
    mlflow.log_metric("val_auc", val_auc)
    
    # Log model artifact to registry
    mlflow.sklearn.log_model(
        sk_model=model,
        artifact_path="model",
        registered_model_name="FraudDetectionClassifier"
    )
```"""
                }
            ]
        },
        {
            "order": 8,
            "title": "High-Performance Model Serving",
            "description": "FastAPI async inference endpoints, ONNX Runtime acceleration, dynamic batching, and Docker containerization.",
            "chapters": [
                {
                    "order": 1,
                    "title": "Low-Latency Inference with ONNX Runtime & FastAPI",
                    "description": "Convert trained models to ONNX graphs and serve sub-10ms predictions asynchronously.",
                    "duration_minutes": 50,
                    "content": """# ONNX Runtime Inference Microservice

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import onnxruntime as ort
import numpy as np

app = FastAPI(title="Real-Time Fraud Scoring Engine")

# Load ONNX graph at startup
session = ort.InferenceSession("models/fraud_model.onnx")
input_name = session.get_inputs()[0].name

class PredictionRequest(BaseModel):
    features: list[float]

@app.post("/predict")
async def predict(payload: PredictionRequest):
    if len(payload.features) != 20:
        raise HTTPException(status_code=400, detail="Expected exactly 20 features.")

    input_data = np.array([payload.features], dtype=np.float32)
    raw_outputs = session.run(None, {input_name: input_data})
    
    probability = float(raw_outputs[1][0][1])
    return {
        "fraud_probability": round(probability, 4),
        "is_fraud": probability >= 0.75
    }
```"""
                }
            ]
        },
        {
            "order": 9,
            "title": "Model Monitoring & Drift Detection in Production",
            "description": "Data drift (KS test, PSI), Concept drift, Evidently AI dashboards, and automated retraining triggers.",
            "chapters": [
                {
                    "order": 1,
                    "title": "Detecting Data & Concept Drift with Population Stability Index",
                    "description": "Calculate PSI thresholds and alert on statistical distribution divergence.",
                    "duration_minutes": 40,
                    "content": """# Population Stability Index (PSI) Drift Calculation

$$PSI = \\sum \\left( (\\text{Actual}\\% - \\text{Expected}\\%) \\times \\ln\\left(\\frac{\\text{Actual}\\%}{\\text{Expected}\\%}\\right) \\right)$$

- **PSI < 0.1**: No significant distribution shift (Normal).
- **0.1 $\le$ PSI < 0.2**: Moderate shift detected (Investigate).
- **PSI $\ge$ 0.2**: Severe drift (Trigger automated pipeline retraining)."""
                }
            ]
        },
        {
            "order": 10,
            "title": "Continuous Training & CI/CD for Machine Learning",
            "description": "CML/CD4ML, automated model regression testing, shadow deployments, and Canary rollouts.",
            "chapters": [
                {
                    "order": 1,
                    "title": "Canary & Shadow Deployments for Production Models",
                    "description": "Route live production traffic safely to candidate models without risking user experience.",
                    "duration_minutes": 40,
                    "content": """# Safe Deployment Strategies for ML

## 1. Shadow Deployment
Production traffic is mirrored: the existing legacy model serves real user responses while the candidate model processes the identical payload in the background to validate latency and accuracy under real conditions.

## 2. Canary Deployment
Route a small percentage of user traffic (e.g. 5%) to the new candidate model, monitoring error rates, fallback triggers, and conversion metrics before ramping traffic to 100%."""
                }
            ]
        }
    ],
    "assessment": {
        "title": "Machine Learning Engineering & MLOps Certification Exam",
        "description": "Demonstrate expertise in bias-variance tradeoffs, ensemble gradient boosting, feature pipelines, MLOps registries, and drift detection.",
        "passing_score": 70,
        "time_limit_minutes": 25,
        "questions": [
            {
                "question_text": "What fundamental effect does L1 Regularization (Lasso) have on model coefficients compared to L2 Regularization (Ridge)?",
                "question_type": "single",
                "explanation": "L1 regularization drives non-essential feature weights to exact zero due to the sharp diamond geometry of the L1 norm constraint, performing automatic feature selection.",
                "points": 20,
                "options": [
                    {"text": "L1 drives non-essential weights to exact zero, performing feature selection", "is_correct": True},
                    {"text": "L1 shrinks all weights uniformly without ever reaching zero", "is_correct": False},
                    {"text": "L1 increases model variance", "is_correct": False},
                    {"text": "L1 can only be used with categorical variables", "is_correct": False}
                ]
            },
            {
                "question_text": "How does Gradient Boosting sequentially train trees compared to Random Forest Bagging?",
                "question_type": "single",
                "explanation": "Boosting trains trees sequentially where each successive tree predicts the negative gradient (residuals) of the loss function, reducing model bias.",
                "points": 20,
                "options": [
                    {"text": "Trees are trained sequentially to fit the residual errors of the previous ensemble", "is_correct": True},
                    {"text": "Trees are trained completely independently in parallel", "is_correct": False},
                    {"text": "Trees are trained on random subsets of columns only", "is_correct": False},
                    {"text": "Each tree is inverted to calculate inverse covariance", "is_correct": False}
                ]
            },
            {
                "question_text": "Why must feature standardizers (e.g. StandardScaler) be fit ONLY on training data inside a Pipeline?",
                "question_type": "single",
                "explanation": "Fitting the scaler on the entire dataset leaks distribution parameters (mean and variance) from the test set into the model, producing overly optimistic evaluation metrics.",
                "points": 20,
                "options": [
                    {"text": "To prevent data leakage from the test set into the training phase", "is_correct": True},
                    {"text": "Because StandardScaler cannot process floating-point numbers", "is_correct": False},
                    {"text": "To speed up disk read performance", "is_correct": False},
                    {"text": "StandardScaler requires GPU acceleration", "is_correct": False}
                ]
            },
            {
                "question_text": "What does a Population Stability Index (PSI) value greater than 0.2 indicate in production model monitoring?",
                "question_type": "single",
                "explanation": "A PSI above 0.2 indicates significant data distribution shift (drift) between baseline training data and production inference data, necessitating model retraining.",
                "points": 20,
                "options": [
                    {"text": "Significant data distribution drift, requiring model retraining", "is_correct": True},
                    {"text": "Perfect model calibration and zero error", "is_correct": False},
                    {"text": "High memory leak on the inference server", "is_correct": False},
                    {"text": "A network timeout in MLflow", "is_correct": False}
                ]
            },
            {
                "question_text": "What is the primary benefit of a Shadow Deployment for machine learning models?",
                "question_type": "single",
                "explanation": "Shadow deployments send real production traffic to a candidate model without returning its predictions to users, allowing validation of latency and accuracy with zero business risk.",
                "points": 20,
                "options": [
                    {"text": "Validating model performance and latency on live traffic with zero business risk to end users", "is_correct": True},
                    {"text": "Reducing training time by half", "is_correct": False},
                    {"text": "Deleting legacy checkpoints automatically", "is_correct": False},
                    {"text": "Encrypting the database connection string", "is_correct": False}
                ]
            }
        ]
    }
}
