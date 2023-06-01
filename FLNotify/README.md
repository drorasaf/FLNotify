# FLNotify

This package is microservice that is able to identify malicious activity on federated learning based
on previous actions and data of the clients.
The package comes with predefined model of FLDetector, however it also provides the infrastructure
to use any other type of validation.
The end result of the microservice is exposing an endpoint to be able to communicate with the
federated learning on the one hand and to send messages to a message queue on the other hand.

## Run tests

pytest tests

## Create Docker

`docker build . -t drorasaf/flnotify`

### Deploy to kubernetes

First create a docker based on [Create Docker](#Create Docker)

`kubectl apply -f deployment.yaml`
