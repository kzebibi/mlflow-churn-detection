


```bash 
mlflow ui


## MLflow project cli
mlflow run . --experiment-name churn-detection
mlflow run -e forest . --experiment-name churn-detection -P n=400 -P d=20
mlflow run -e logistic . --experiment-name churn-detection -P c=2 -P p="l1"
mlflow run -e xgboost . --experiment-name churn-detection -P n=400 -P lr=0.1 -P d=20

```


To install `make`  on Windows, you can follow these steps:

1. **Install Chocolatey** (if you haven't already):
   - Open an elevated Command Prompt (Run as Administrator).
   - Run the following command to install Chocolatey:
     ```bash
     @"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"
     ```

2. **Install Make**:
   - After installing Chocolatey, you can install `make` by running the following command in the Command Prompt:
     ```bash
     choco install make
     ```

3. **Verify Installation**:
   - Open Command Prompt and run:
     ```bash
     make --version
     ```
   - This should display the version of `make` installed.


### Example Usage in Bash

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

### Explanation:
- **`make`**: This command invokes the Makefile.
- **`mlflow-forest`, `mlflow-logistic`, `mlflow-xgboost`**: These are the targets defined in the Makefile.
- **`EXPERIMENT_NAME`, `N`, `D`, `C`, `P`, `LR`**: These are the parameters you can set when calling the make command. You can replace the values with whatever you need for your specific experiment.

### Complete Example:
If you want to run the `mlflow-forest` target with specific parameters, you would execute:
```bash
make mlflow-forest EXPERIMENT_NAME="churn-detection" N=400 D=20
```

This command will run the MLflow project with the specified parameters for the `forest` experiment.