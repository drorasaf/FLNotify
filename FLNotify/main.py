from http import HTTPStatus

from flask import Flask, request

app = Flask(__name__)
# For running WSGI
app.config["APPLICATION_ROOT"] = "/api/v1"

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


@app.route("/model/register", methods=["POST"])
def register_model():
    """This is the precursor to any other operation when interacting
    with the system to be able to keep track about the models"""
    data = request.get_json(force=True)
    model_id = data["model_id"]
    app.logger.info(f"Registerting model: {model_id}")
    if model_check_exist(model_id):
        return HTTPStatus.CONFLICT
    model_init(model_id)
    return "OK", HTTPStatus.OK


@app.route("/model/update", methods=["POST"])
def update_model():
    """Returns boolean value specifying if the update provided is reasonable
    or not based on the algorithm that has been initialized with"""
    data = request.get_json(force=True)

    model_id = data["model_id"]
    weights = data["weights"]

    app.logger.info(f"Update weights to model: {model_id}")
    app.logger.debug(f"weights: {weights}")

    if not model_check_exist(model_id):
        return HTTPStatus.NOT_FOUND

    model_update_data(model_id, weights)
    model_data = model_get_data(model_id)

    app.logger.debug(f"Run validation on: {model_data}")
    # TBD: run validation model on updates
    return True, HTTPStatus.OK


if __name__ == "__main__":
    app.run()
