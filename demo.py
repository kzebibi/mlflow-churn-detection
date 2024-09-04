import mlflow
import os
import time
import argparse

import mlflow.experiments


def eval(param_1, param_2):
    return (param_1 + param_2) / 2


def main(param_1, param_2):

    mlflow.set_experiment(experiment_name="demo-example")
    with mlflow.start_run() as run:
        mlflow.set_tag("version", "1.0.0")
        mlflow.log_param("param_1", param_1)
        mlflow.log_param("param_2", param_2)
        mlflow.log_metric("mean", eval(param_1=param_1, param_2=param_2))

        os.makedirs("dummy-folder", exist_ok=True)
        with open("./dummy-folder/example.txt", "w") as f:
            f.write(f"Created at: {time.asctime()}")

        mlflow.log_artifacts(local_dir="dummy-folder")


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--param_1", "-p1", default=10, type=int)
    parser.add_argument("--param_2", "-p2", default=20, type=int)
    args = parser.parse_args()

    main(args.param_1, args.param_2)
