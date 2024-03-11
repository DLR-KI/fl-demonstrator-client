---
title: Home
hide: navigation
---

<!-- markdownlint-disable-next-line MD025 -->
# Federated Learning Client Base Image

This is a small Python package designed to simplify development of a Federated Learning platform client in Python.
Its includes the necessary communication endpoint as well as aids in the interaction between the client and the server.

This project is a component of the Federated Learning (FL) platform, serving as a proof of concept for the [Catena-X](https://catena-x.net/en) project.
The FL platform aims to demonstrate the potential of federated learning in a practical, real-world context.

For a comprehensive understanding of the FL platform, please refer to the official [FL platform documentation](https://dlr-ki.github.io/fl-documentation).

A complete list of all repositories relevant to the FL platform can be found [here](https://dlr-ki.github.io/fl-documentation#repositories).

## Get Started

A great starting point for this package is the MNIST example client [tutorial](https://dlr-ki.github.io/fl-documentation/tutorial).
The [MNIST example client](https://github.com/DLR-KI/fl-demonstrator-mnist) source code is also open source.
For Python client developer it is advised to start your new client development based on the MNIST example client.

## Environment Variables

| Variable                                    | Default                           | Description                                             |
|:--------------------------------------------|:----------------------------------|:--------------------------------------------------------|
| `FL_CLIENT_ADDITIONAL_SYS_PATH`             | empty                             | Additional client sys path seperated by an colon (`:`). |
| `FL_CLIENT_SERVER_HOST`                     | `0.0.0.0`                         | Client server hostname.                                 |
| `FL_CLIENT_SERVER_PORT`                     | `8101`                            | Client server port.                                     |
| `FL_CLIENT_SETTINGS_MODULE`                 | `dlr.fl.client.settings.Settings` | Client settings module.                                 |
| `FL_DEMONSTRATOR_BASE_URL`                  | `http://localhost:8000`           | Base URL of the FL Demonstrator server.                 |
| `FL_DEMONSTRATOR_TRAINING_SCRIPT_EXECUTOR`  | `python`                          | Path to the script executor.                            |
| `FL_DEMONSTRATOR_TRAINING_SCRIPT_PATH`      | `src/main.py`                     | Path to the training script.                            |
| `FL_DEMONSTRATOR_TRAINING_WORKING_DIRETORY` | `.`                               | Working directory for the training script.              |
