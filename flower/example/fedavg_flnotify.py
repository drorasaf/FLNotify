import json
import os
import random
import string
from typing import Dict, List, Optional, Tuple, Union

import flwr as fl
import numpy as np
import requests
from flwr.common import FitRes, Parameters, Scalar, parameters_to_ndarrays
from flwr.server.client_proxy import ClientProxy


def get_random_string(length):
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(length))


class FLNotifyFedAvg(fl.server.strategy.FedAvg):
    """FedAverage integration with flnotify.""" 
    flnotify_url = os.environ["FLNOTIFY_URI"]
    flnotify_path = "/api/v1/model/update"
    model_id = get_random_string(8)

    def aggregate_fit(
        self,
        server_round: int,
        results: List[Tuple[ClientProxy, FitRes]],
        failures: List[Union[Tuple[ClientProxy, FitRes], BaseException]],
    ) -> Tuple[Optional[Parameters], Dict[str, Scalar]]:
        """Aggregate fit results using weighted average."""
        weights = [
            (parameters_to_ndarrays(fit_res.parameters), fit_res.num_examples)
            for _, fit_res in results
        ]
        try:
            malicious_indexes = self.call_flnotify(weights)
            fl.common.logger.FLOWER_LOGGER.info("Malicious indexes for this round: %s", str(malicious_indexes))
            malicious_results = [results[x] for x in malicious_indexes]
            validated_results = [x for x in results if x not in malicious_results]
        except requests.exceptions.HTTPError:
            validated_results = results

        return super().aggregate_fit(
            server_round=server_round, results=validated_results, failures=failures
        )

    def call_flnotify(self, weights):
        data = json.dumps(
            {"model_id": self.model_id, "weights": weights}, cls=NumpyEncoder
        )
        resp = requests.post(
            f"{self.flnotify_url}{self.flnotify_path}", json=data, timeout=20
        )
        resp.raise_for_status()
        return resp.json()


class NumpyEncoder(json.JSONEncoder):
    """Special json encoder for numpy types"""

    def default(self, o):
        if isinstance(o, np.integer):
            return int(o)
        if isinstance(o, np.floating):
            return float(o)
        if isinstance(o, np.ndarray):
            return o.tolist()
        return json.JSONEncoder.default(self, o)
