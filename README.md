# FLNotify - Thesis

This code is part of thesis work to establish the FLNotify framework as a keycomponent in future federated learning architectures.

This repository is composed of 4 different components:
1. infrastructure which contains the code for easily spinning up and down on AWS the required components for FedLess
1. FLNotify is the package which provides notification for the security
1. Modified FedLess version to include interaction with FLNotify to allow easy notification to security
1. Flower based code with interaction to FLNotify, enabling another framework to integrate with this.


## Get AWS credentials

Run:
`pip install awscli`
`aws configure`

## Installation

1. Download terraform based on your platform from HashiCorp.
1. Go to directory `cd infrastructure`
1. Get AWS credentials
1. Run `terraform apply`

## Teardown of infrastructure

1. Go to Directory `cd infrastructure`
1. Get AWS credentials
1. Run `terraform destroy`

## Deploy FedLess

Assuming installation has already happened, if not, please see [Installation](#Installation)

1. Login to kubectl, run: `aws eks update-kubeconfig --region region-code --name my-cluster`
1. Go to Fedless\kubernetes
1. Go to data-file-store
1. run `kubectl -f deployment.yaml`
1. run `kubectl -f service.yaml`
1. Go to parameter-server
1. create a helm package: `helm package parameter-server`
1. deploy helm chart: `helm install -f parameter-server/values.yaml parameter-store parameter-server-0.1.0.tgz`
1. deploy openwhisk on the cluster: `??`
1. deploy invoker `??`
1. deploy aggregator: `?`

## setup clients ??

## Get Data

Run:
1. `git clone https://github.com/andreas-grafberger/leaf.git`
1. `cd data\femnist`
1. `./preprocess.sh -s niid --sf 0.25 -k 100 -t sample --smplseed 1549786595 --spltseed 1549786796 --nochecksum`
1. `cd ../shakespeare`
1. `./preprocess.sh -s niid --sf 1.0 -k 64 -tf 0.9 -t sample --nochecksum`

## Run an experiment

Go to scripts and run any of the existing experiments

## Run an experiment on Flower

TBD
