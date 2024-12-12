# Catalyst Loan Broker

This solution demonstrates the capabilities provided by the Workflow, Pubsub, and State Catalyst APIs through a python-based loan broker application. The end-to-end solution is comprised of five services:

- **loan-broker**: Contains the workflow definition and associated activities for running a credit look up and then executing requests to three banks to get rate quotes for a loan based on the amount and term.
- **credit-bureau**: Receives direct invocation requests sent by the loan-broker using the Invocation API to return a credit score that will be used when reaching out to each bank to retrieve a quote.
- **riverstone-bank, titanium trust, and union vault**: Each of these apps represents a bank that will be running the loan request received in order to return a loan approved/denied status with a rate quote.
- **quote-aggregator**: Subscribes to messages published by the loan-broker and stores them in a database through the Catalyst State API.

![solutions_architecture](https://raw.githubusercontent.com/trey-rosius/loan_broker_application/main/assets/solutions_architecture.png)

## App prerequisites

The solution is comprised of python services:

- Install [Python3](https://www.python.org/downloads/)

The payment app makes use of an HTTP output binding pointing to Square. Follow the steps below to configure:

## Deploy Catalyst resources

Replace `unique-project-name` with a name for your workflow project

```bash
export PROJECT_NAME="unique-project-name"
```

Install dependencies for the applications

```bash
pip3 install -r requirements.txt
```

Run this script to deploy a catalyst project, scaffold all of the required App IDs and scaffold the dev config file which can be used to run and test the apps locally

```bash
python3 run.py
```

## Connect local app using dev config file

After the above script runs to completion, use the dev config file to run the local apps and connect to Catalyst

```bash
diagrid dev start
```

## Use the APIs

A `test.rest` file is available at the root of this repository and can be used with the VS Code `Rest Client` extension.
    ![Rest Client](/images/rest-client.png)