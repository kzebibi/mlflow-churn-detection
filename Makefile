install:
	pip install --upgrade pip && \
		pip install -r requirements.txt

mlflow:
	mlflow ui

mlflow-experiment:
	mlflow run . --experiment-name churn-detection	

# mlflow-experiment:
# 	mlflow run . --experiment-name $(EXPERIMENT_NAME)

mlflow-forest:
	mlflow run -e forest . --experiment-name $(EXPERIMENT_NAME) -P n=$(N) -P d=$(D)

mlflow-logistic:
	mlflow run -e logistic . --experiment-name $(EXPERIMENT_NAME) -P c=$(C) -P p="$(P)"

mlflow-xgboost:
	mlflow run -e xgboost . --experiment-name $(EXPERIMENT_NAME) -P n=$(N) -P lr=$(LR) -P d=$(D)

test:
	python -m pytest -vv --cov=main --cov=mylib test_*.py

format:	
	black . --exclude venv
# black *.py
lint:
	pylint --disable=R,C --ignore-patterns=test_.*?py *.py **/*.py

container-lint:
	docker run --rm -i hadolint/hadolint < Dockerfile

refactor: format lint

deploy:
	# deploy goes here

all: install lint test format deploy