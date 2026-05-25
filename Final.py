import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import (
    train_test_split,
    RandomizedSearchCV
)

from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    classification_report,
    ConfusionMatrixDisplay
)

from sklearn.linear_model import LogisticRegression

from sklearn.ensemble import (
    RandomForestClassifier,
    VotingClassifier
)

from sklearn.tree import DecisionTreeClassifier

from sklearn.neighbors import KNeighborsClassifier

from imblearn.pipeline import Pipeline

from imblearn.over_sampling import SMOTE

from sklearn.preprocessing import StandardScaler

from xgboost import XGBClassifier

import pickle

df = pd.read_csv("good_autism_dataset_2000.csv")

print(df.shape)

print(df.head())

print(df.info())

print(df.describe())


print(df.isnull().sum())

print(df.duplicated().sum())

print(df.dtypes)

df['total_score'] = df[
    [f"A{i}_Score" for i in range(1, 11)]
].sum(axis=1)

print(df.head())

plt.figure(figsize=(8,5))

sns.histplot(df['age'], kde=True)

plt.title("Age Distribution")

plt.show()

plt.figure(figsize=(8,5))

sns.histplot(df['total_score'], kde=True)

plt.title("Total Score Distribution")

plt.show()

plt.figure(figsize=(6,4))

sns.countplot(x='Class/ASD', data=df)

plt.title("ASD Distribution")

plt.show()

plt.figure(figsize=(8,5))

sns.boxplot(
    x='Class/ASD',
    y='total_score',
    data=df
)

plt.title("Total Score vs ASD")

plt.show()

df = df.dropna(subset=['Class/ASD']).copy()

X = pd.get_dummies(
    df.drop(columns=['Class/ASD']),
    drop_first=True
)

y = df['Class/ASD'].map({
    'NO': 0,
    'YES': 1
})

print(X.head())

print(y.head())

plt.figure(figsize=(12,10))

sns.heatmap(
    X.corr(),
    cmap="coolwarm"
)

plt.title("Correlation Heatmap")

plt.show()

y = df['Class/ASD'].astype(int)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print(X_train.shape)

print(X_test.shape)

print(X_train.shape)

print(X_test.shape)

knn = Pipeline([

    ("smote", SMOTE(random_state=42)),

    ("scaler", StandardScaler()),

    ("model", KNeighborsClassifier(
        n_neighbors=3,
        weights='distance',
        metric='manhattan'
    ))
])

knn.fit(X_train, y_train)

y_pred_knn = knn.predict(X_test)

knn_accuracy = accuracy_score(
    y_test,
    y_pred_knn
)

print("KNN Accuracy:", knn_accuracy)

print(confusion_matrix(
    y_test,
    y_pred_knn
))

print(classification_report(
    y_test,
    y_pred_knn
))


lr = LogisticRegression(max_iter=1000)

lr.fit(X_train, y_train)

y_pred_lr = lr.predict(X_test)

lr_accuracy = accuracy_score(
    y_test,
    y_pred_lr
)

print("Logistic Accuracy:", lr_accuracy)

print(confusion_matrix(
    y_test,
    y_pred_lr
))

print(classification_report(
    y_test,
    y_pred_lr
))

rf = RandomForestClassifier(
    n_estimators=200,
    max_depth=10,
    random_state=42
)

rf.fit(X_train, y_train)

y_pred_rf = rf.predict(X_test)

rf_accuracy = accuracy_score(
    y_test,
    y_pred_rf
)

print("RF Accuracy:", rf_accuracy)

print(confusion_matrix(
    y_test,
    y_pred_rf
))

print(classification_report(
    y_test,
    y_pred_rf
))

pipeline = Pipeline([

    ("smote", SMOTE(random_state=42)),

    ("scaler", StandardScaler()),

    ("model", XGBClassifier(
        eval_metric='logloss',
        random_state=42
    ))
])

param_grid = {

    "model__n_estimators": [200, 300],

    "model__max_depth": [3, 5, 7],

    "model__learning_rate": [0.05, 0.1],
}

search = RandomizedSearchCV(

    pipeline,

    param_grid,

    n_iter=5,

    cv=5,

    scoring='accuracy',

    random_state=42
)

search.fit(X_train, y_train)


best_model = search.best_estimator_

y_pred_xgb = best_model.predict(X_test)

xgb_accuracy = accuracy_score(
    y_test,
    y_pred_xgb
)

print("XGBoost Accuracy:", xgb_accuracy)

print(confusion_matrix(
    y_test,
    y_pred_xgb
))

print(classification_report(
    y_test,
    y_pred_xgb
))

pipeline_dt = Pipeline([

    ('smote', SMOTE(random_state=42)),

    ('scaler', StandardScaler()),

    ('dt', DecisionTreeClassifier(
        random_state=42,
        max_depth=5
    ))
])

pipeline_dt.fit(X_train, y_train)

y_pred_dt = pipeline_dt.predict(X_test)

dt_accuracy = accuracy_score(
    y_test,
    y_pred_dt
)

print("Decision Tree Accuracy:", dt_accuracy)

print(confusion_matrix(
    y_test,
    y_pred_dt
))

print(classification_report(
    y_test,
    y_pred_dt
))

voting_model = VotingClassifier(

    estimators=[

        ('lr', lr),

        ('rf', rf),

        ('dt', pipeline_dt),

        ('knn', knn),

        ('xgb', best_model)

    ],

    voting='hard'
)

voting_model.fit(X_train, y_train)
y_pred_vote = voting_model.predict(X_test)

vote_accuracy = accuracy_score(
    y_test,
    y_pred_vote
)

print("Voting Accuracy:", vote_accuracy)

print(confusion_matrix(
    y_test,
    y_pred_vote
))

print(classification_report(
    y_test,
    y_pred_vote
))

results = {

    'Logistic Regression': lr_accuracy,

    'Random Forest': rf_accuracy,

    'Decision Tree': dt_accuracy,

    'KNN': knn_accuracy,

    'XGBoost': xgb_accuracy,

    'Voting': vote_accuracy
}

print(results)

models = list(results.keys())

accuracies = list(results.values())

plt.figure(figsize=(12,6))

plt.bar(models, accuracies)

plt.title("Model Accuracy Comparison")

plt.xlabel("Models")

plt.ylabel("Accuracy")

for i, v in enumerate(accuracies):

    plt.text(i, v + 0.01, f"{v:.2f}", ha='center')

plt.ylim(0, 1.1)

plt.show()

ConfusionMatrixDisplay.from_estimator(
    voting_model,
    X_test,
    y_test
)

plt.title("Voting Classifier Confusion Matrix")

plt.show()

# %%
import pickle

pickle.dump(voting_model, open("fresh_model.pkl", "wb"))

import joblib

joblib.dump(voting_model, "fresh_model.pkl")