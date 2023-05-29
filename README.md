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

1. Run kubernetes scripts from FedLess TBD?


## Run an experiment

Go to scripts and run any of the existing experiments

## Run an experiment on Flower

TBD
