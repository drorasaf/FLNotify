"""Example how to integrate server with flnotify."""
import flwr as fl

from dotenv import load_dotenv
load_dotenv()
from fedavg_flnotify import FLNotifyFedAvg

strategy = FLNotifyFedAvg()

fl.server.start_server(
    server_address="0.0.0.0:8080",
    config=fl.server.ServerConfig(num_rounds=200),
    strategy=strategy,
)
