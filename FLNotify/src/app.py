"""Microservice for federated learning update validation."""
import json
import os
from http import HTTPStatus

import boto3
import botocore
from flask import Flask, request
from dotenv import load_dotenv

#from fldetector import FLDetector
from validation import AlwaysFailValidation, AlwaysPassValidation

def queue_client(queue_type):
    if queue_type == "elasticmq":
        return boto3.resource(
            "sqs",
            endpoint_url="http://localhost:9324",
            region_name="elasticmq",
            aws_secret_access_key="x",
            aws_access_key_id="x",
            use_ssl=False,
        )
    if queue_type == "sqs":
        return boto3.resource("sqs")

    raise ValueError("Unknown value: {queue_type} for initialization of queue")


models = {}
def model_init(model_id):
    models[model_id] = []


def model_check_exist(model_id):
    return model_id in models


def model_get_data(model_id):
    return models[model_id]


def model_update_data(model_id, weights):
    models[model_id].append(weights)
    models[model_id] = models[model_id][-50:]


def transform_data(model_results):
    """Returns a list of lists results where all results that have been sent are for client 0 are in
    index 0, all results for client 1 in index 1, etc."""
    if len(model_results) == 0:
        return model_results

    client_results = []
    for index in range(len(model_results[0])):
        client_results.append([x[index] for x in model_results])
    return client_results


def create_app():
    app = Flask(__name__)
    load_dotenv()

    validators = {
        #"fldetector": FLDetector,
        "fail": AlwaysFailValidation,
        "pass": AlwaysPassValidation
    }
    app.config["VALIDATOR"] = validators[os.environ["FLNOTIFY_VALIDATION"]]()
    app.config["QUEUE_CLIENT"] = queue_client(os.environ["FLNOTIFY_QUEUE_CLIENT"])
    app.config["QUEUE_NAME"] = os.environ["FLNOTIFY_QUEUE_NAME"]
    return app


def send_message(client, name, message_body):
    """Send a message to an Amazon SQS queue."""
    queue = client.get_queue_by_name(QueueName=name)

    try:
        response = queue.send_message(MessageBody=message_body)
    except botocore.exceptions.ClientError as error:
        app.logger.error("Unable to send message: %s", error)
        raise error
    return response


app = create_app()


@app.route("/api/v1/model/update", methods=["POST"])
def update_model():
    """Returns boolean value specifying if the update provided is reasonable
    or not based on the algorithm that has been initialized with"""
    data_str = request.get_json()
    data = json.loads(data_str)

    app.logger.debug("data type %s", type(data))
    model_id = data["model_id"]
    weights = data["weights"]

    app.logger.info("Update weights to model: %s", model_id)
    app.logger.debug("weights: %d", len(weights))

    if not model_check_exist(model_id):
        model_init(model_id)

    model_update_data(model_id, weights)
    model_data = model_get_data(model_id)
    client_results = transform_data(model_data)

    assert len(model_data[0]) == len(client_results)
    app.logger.debug("size: %d type: %s", len(model_data),type(model_data))
    app.logger.debug("size: %d type: %s", len(model_data[0]),type(model_data[0]))
    app.logger.debug("size: %d type: %s", len(client_results), type(client_results))

    suspicious_clients = app.config["VALIDATOR"].validate_all_clients(client_results)
    if suspicious_clients:
        send_message(
            app.config["QUEUE_CLIENT"],
            app.config["QUEUE_NAME"],
            json.dumps(suspicious_clients),
        )
    return suspicious_clients, HTTPStatus.OK


if __name__ == "__main__":
    app.run(port=5001)
