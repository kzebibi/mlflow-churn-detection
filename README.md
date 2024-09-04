Here's an improved version of your README file, with better organization, clarity, and formatting:

```markdown
# MLflow Project Documentation

## Overview
This document provides instructions for running MLflow projects, installing necessary tools, and using the MLflow models.

## MLflow UI
To start the MLflow UI, run the following command:
```bash
mlflow ui
```

## MLflow Project CLI
You can run various MLflow projects using the following commands:

```bash
# Run the main project
mlflow run . --experiment-name churn-detection

# Run specific experiments with parameters
mlflow run -e forest . --experiment-name churn-detection -P n=400 -P d=20
mlflow run -e logistic . --experiment-name churn-detection -P c=2 -P p="l1"
mlflow run -e xgboost . --experiment-name churn-detection -P n=400 -P lr=0.1 -P d=20
```

## Installing `make` on Windows
To install `make`, follow these steps:

1. **Install Chocolatey** (if not already installed):
   - Open an elevated Command Prompt (Run as Administrator).
   - Execute the following command:
     ```bash
     @"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"
     ```

2. **Install Make**:
   - After installing Chocolatey, run:
     ```bash
     choco install make
     ```

3. **Verify Installation**:
   - Check the installation by running:
     ```bash
     make --version
     ```
   - This command should display the installed version of `make`.

## Example Usage in Bash
You can use the following commands to run specific targets defined in the Makefile:

1. **For the `mlflow-forest` target:**
   ```bash
   make mlflow-forest EXPERIMENT_NAME="churn-detection" N=400 D=20
   ```

2. **For the `mlflow-logistic` target:**
   ```bash
   make mlflow-logistic EXPERIMENT_NAME="churn-detection" C=2 P="l1"
   ```

3. **For the `mlflow-xgboost` target:**
   ```bash
   make mlflow-xgboost EXPERIMENT_NAME="churn-detection" N=400 LR=0.1 D=20
   ```

### Explanation of Parameters
- **`make`**: Invokes the Makefile.
- **Targets**: `mlflow-forest`, `mlflow-logistic`, `mlflow-xgboost` are defined in the Makefile.
- **Parameters**: `EXPERIMENT_NAME`, `N`, `D`, `C`, `P`, `LR` can be customized for your experiments.

## Serving MLflow Models
To serve an MLflow model, use the following command:

```bash
mlflow models serve -m "PATH" --port 8000 --env-manager local
```

### Accessing the Model
Once the model is served, you can access it at:
```
http://localhost:8000/invocations
```

## Using Postman
You can use Postman to send requests to the model. Here’s an example of the JSON data format to send:

### Example Data
```json
{
    "dataframe_split": {
        "columns": [
            "Age", 
            "CreditScore", 
            "Balance", 
            "EstimatedSalary", 
            "Gender_Male", 
            "Geography_Germany", 
            "Geography_Spain", 
            "HasCrCard", 
            "Tenure", 
            "IsActiveMember", 
            "NumOfProducts"
        ],
        "data": [
            [-0.7541830079917924, 0.5780143566720919, 0.11375998165198585, -0.14673040749854463, 0.0, 0.0, 0.0, 0.0, 2.0, 0.0, 2.0]
        ]
    }
}
```


### Multiple Samples
```json
{
    "dataframe_split": {
        "columns": [
            "Age",
            "CreditScore",
            "Balance",
            "EstimatedSalary",
            "Gender_Male",
            "Geography_Germany",
            "Geography_Spain",
            "HasCrCard",
            "Tenure",
            "IsActiveMember",
            "NumOfProducts"
        ],
        "data": [
            [-0.7541830079917924, 0.5780143566720919, 0.11375998165198585, -0.14673040749854463, 0.0, 0.0, 0.0, 0.0, 2.0, 0.0, 2.0],
            [-0.5605884106597949, 0.753908347743766, 0.7003528882054108, 1.6923927520037099, 0.0, 1.0, 0.0, 1.0, 9.0, 1.0, 1.0],
            [0.11699268000219652, -0.3221490094005933, 0.5222180917013974, -0.8721429873346316, 1.0, 1.0, 0.0, 1.0, 5.0, 0.0, 2.0],
            [0.6977764719981892, -0.7256705183297281, -1.2170740485175422, 0.07677206232885857, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 2.0]
        ]
    }
}
```
- Use Postman to test the API endpoints easily.

![alt text](image-1.png)


## Sending Requests
### Using `curl`
```bash
curl -X POST \
  http://localhost:8000/invocations \
  -H 'Content-Type: application/json' \
  -d '{
    "dataframe_split": {
        "columns": [
            "Age",
            "CreditScore",
            "Balance",
            "EstimatedSalary",
            "Gender_Male",
            "Geography_Germany",
            "Geography_Spain",
            "HasCrCard",
            "Tenure",
            "IsActiveMember",
            "NumOfProducts"
        ],
        "data": [
            [-0.7541830079917924, 0.5780143566720919, 0.11375998165198585, -0.14673040749854463, 0.0, 0.0, 0.0, 0.0, 2.0, 0.0, 2.0],
            [-0.5605884106597949, 0.753908347743766, 0.7003528882054108, 1.6923927520037099, 0.0, 1.0, 0.0, 1.0, 9.0, 1.0, 1.0],
            [0.11699268000219652, -0.3221490094005933, 0.5222180917013974, -0.8721429873346316, 1.0, 1.0, 0.0, 1.0, 5.0, 0.0, 2.0],
            [0.6977764719981892, -0.7256705183297281, -1.2170740485175422, 0.07677206232885857, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 2.0]
        ]
    }
}'
```

### Using PowerShell
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/invocations" -Method Post -Headers @{"Content-Type" = "application/json"} -Body '{
    "dataframe_split": {
        "columns": [
            "Age",
            "CreditScore",
            "Balance",
            "EstimatedSalary",
            "Gender_Male",
            "Geography_Germany",
            "Geography_Spain",
            "HasCrCard",
            "Tenure",
            "IsActiveMember",
            "NumOfProducts"
        ],
        "data": [
            [-0.7541830079917924, 0.5780143566720919, 0.11375998165198585, -0.14673040749854463, 0.0, 0.0, 0.0, 0.0, 2.0, 0.0, 2.0],
            [-0.5605884106597949, 0.753908347743766, 0.7003528882054108, 1.6923927520037099, 0.0, 1.0, 0.0, 1.0, 9.0, 1.0, 1.0],
            [0.11699268000219652, -0.3221490094005933, 0.5222180917013974, -0.8721429873346316, 1.0, 1.0, 0.0, 1.0, 5.0, 0.0, 2.0],
            [0.6977764719981892, -0.7256705183297281, -1.2170740485175422, 0.07677206232885857, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 2.0]
        ]
    }
}'
```

## Additional Notes
- Ensure that the MLflow server is running before sending requests.

## MLflow Model Registry

```bash
mlflow models serve -m "models:/forest_best_acc/Staging" --port 8080 --env-manager local

mlflow server --host 0.0.0.0 --port 5050 --backend-store-uri mysql://root:jiji@localhost:3306/mlflow_logs --default-artifact-root ./mlruns
```