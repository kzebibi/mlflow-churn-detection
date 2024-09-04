import mlflow


try:
    exp_id = mlflow.create_experiment("test")
    print(exp_id)

except:
    pass

exp = mlflow.set_experiment("test_something")


with mlflow.start_run() as run:
    pass

mlflow.log_param("param-1", 10)
mlflow.log_params({"param-1": 10, "param-2": 20})


mlflow.log_param("accuracy", 0.8)
mlflow.log_params({"accuracy": 0.9, "f1": 0.68})
