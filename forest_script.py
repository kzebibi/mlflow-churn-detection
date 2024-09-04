## main
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from imblearn.over_sampling import SMOTE
from PIL import Image
import joblib
import mlflow
import fire

## skelarn -- preprocessing
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn_features.transformers import DataFrameSelector
from sklearn.ensemble import RandomForestClassifier

## skelarn -- models
# from sklearn.neighbors import KNeighborsClassifier
# from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

## sklearn -- metrics
from sklearn.metrics import f1_score, confusion_matrix, accuracy_score, auc, roc_curve

os.makedirs("models", exist_ok=True)

## --------------------- Data Preparation ---------------------------- ##

## Read the Dataset
TRAIN_PATH = os.path.join(os.getcwd(), "dataset.csv")
df = pd.read_csv(TRAIN_PATH)

## Drop first 3 features
df.drop(columns=["RowNumber", "CustomerId", "Surname"], axis=1, inplace=True)

## Filtering using Age Feature using threshold
df.drop(index=df[df["Age"] > 80].index.tolist(), axis=0, inplace=True)


## To features and target
X = df.drop(columns=["Exited"], axis=1)
y = df["Exited"]

## Split to train and test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, shuffle=True, random_state=45, stratify=y
)


## --------------------- Data Processing ---------------------------- ##

## Slice the lists
num_cols = ["Age", "CreditScore", "Balance", "EstimatedSalary"]
categ_cols = ["Gender", "Geography"]

ready_cols = list(set(X_train.columns.tolist()) - set(num_cols) - set(categ_cols))


## For Numerical
num_pipeline = Pipeline(
    steps=[
        ("selector", DataFrameSelector(num_cols)),
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ]
)


## For Categorical
categ_pipeline = Pipeline(
    steps=[
        ("selector", DataFrameSelector(categ_cols)),
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("ohe", OneHotEncoder(drop="first", sparse_output=False)),
    ]
)


## For ready cols
ready_pipeline = Pipeline(
    steps=[
        ("selector", DataFrameSelector(ready_cols)),
        ("imputer", SimpleImputer(strategy="most_frequent")),
    ]
)


## combine all
all_pipeline = FeatureUnion(
    transformer_list=[
        ("numerical", num_pipeline),
        ("categorical", categ_pipeline),
        ("ready", ready_pipeline),
    ]
)

## apply
X_train_final = all_pipeline.fit_transform(X_train)
X_test_final = all_pipeline.transform(X_test)


## --------------------- Impalancing ---------------------------- ##

## 1. use algorithm without taking the effect of imbalancing

## 2. prepare class_weights for solving imbalance dataset
vals_count = 1 - (np.bincount(y_train) / len(y_train))
vals_count = vals_count / np.sum(vals_count)  ## normalizing


dict_weights = {}
for i in range(2):  ## 2 classes (0, 1)
    dict_weights[i] = vals_count[i]

## 3. Using SMOTE for over sampling
over = SMOTE(sampling_strategy=0.7)
X_train_resmapled, y_train_resampled = over.fit_resample(X_train_final, y_train)


## --------------------- Modeling ---------------------------- ##

# ## Clear metrics.txt file at the beginning
# with open('metrics.txt', 'w') as f:
#     pass

mlflow.set_tracking_uri('http://localhost:5050/')
def train_model(
    X_train, y_train, plot_name, n_estimators: int, max_depth: int, class_weight=None
):
    """A function to train model given the required train data"""

    mlflow.set_experiment(experiment_name="churn-detection-db")
    with mlflow.start_run() as run:
        mlflow.set_tracking_uri('http://localhost:5050/')
        mlflow.set_tag("clf", "forest")
        clf = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            random_state=53,
            class_weight=class_weight,
        )
        clf.fit(X_train, y_train)

        y_pred_test = clf.predict(X_test_final)

        ## Using f1_score and accuracy_score for test
        acc_score_test = accuracy_score(y_test, y_pred_test)
        f1_score_test = f1_score(y_test, y_pred_test)

        mlflow.log_params({"n_estimators": n_estimators, "max_depth": max_depth})
        mlflow.log_metrics({"accuracy": acc_score_test, "f1_score": f1_score_test})
        mlflow.sklearn.log_model(clf, f"{clf.__class__.__name__}/{plot_name}")

        clf_name = clf.__class__.__name__

        ## Plot the confusion matrix
        plt.figure(figsize=(8, 6))
        sns.heatmap(
            confusion_matrix(y_test, y_pred_test),
            annot=True,
            cbar=False,
            fmt=".2f",
            cmap="Blues",
        )
        plt.title(f"{plot_name}")
        plt.xticks(ticks=np.arange(2) + 0.5, labels=[False, True])
        plt.yticks(ticks=np.arange(2) + 0.5, labels=[False, True])

        # log confusion figure
        conf_fig = plt.gcf()
        mlflow.log_figure(
            figure=conf_fig, artifact_file=f"{plot_name}_conf._matrix.png"
        )
        plt.close()

        # Compute ROC curve and AUC
        fpr, tpr, _ = roc_curve(y_test, y_pred_test)
        roc_auc = auc(fpr, tpr)

        # Plot ROC curve and save it to mlflow
        plt.figure()
        plt.plot(
            fpr,
            tpr,
            color="darkorange",
            lw=2,
            label="ROC curve (area = %0.2f)" % roc_auc,
        )
        plt.plot([0, 1], [0, 1], color="navy", lw=2, linestyle="--")
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel("False Positive Rate")
        plt.ylabel("True Positive Rate")
        plt.title("Receiver Operating Characteristic (ROC) Curve")
        plt.legend(loc="lower right")

        # log the roc curve
        roc_fig = plt.gcf()
        mlflow.log_figure(figure=roc_fig, artifact_file=f"{plot_name}_roc_curve.png")
        plt.close()


def main(n_estimators="300", max_depth="15"):
    # Convert command-line arguments to integers
    n_estimators = int(n_estimators)  # Ensure this is an integer
    max_depth = int(max_depth)  # Ensure this is an integer

    ## 1. without considering the imabalancing data
    train_model(
        X_train=X_train_final,
        y_train=y_train,
        plot_name="without-imbalance",
        n_estimators=n_estimators,
        max_depth=max_depth,
        class_weight=None,
    )

    ## 2. with considering the imabalancing data using class_weights
    train_model(
        X_train=X_train_final,
        y_train=y_train,
        plot_name="with-class-weights",
        n_estimators=n_estimators,
        max_depth=max_depth,
        class_weight=dict_weights,
    )

    ## 3. with considering the imabalancing data using oversampled data (SMOTE)
    train_model(
        X_train=X_train_resmapled,
        y_train=y_train_resampled,
        plot_name=f"with-SMOTE",
        n_estimators=n_estimators,
        max_depth=max_depth,
        class_weight=None,
    )


if __name__ == "__main__":
    fire.Fire(main)
