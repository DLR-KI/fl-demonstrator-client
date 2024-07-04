# SPDX-FileCopyrightText: 2024 Benedikt Franke <benedikt.franke@dlr.de>
# SPDX-FileCopyrightText: 2024 Florian Heinrich <florian.heinrich@dlr.de>
#
# SPDX-License-Identifier: Apache-2.0

from os import environ


class Settings:
    """
    Client settings.
    """

    FL_DEMONSTRATOR_BASE_URL: str = environ.get("FL_DEMONSTRATOR_BASE_URL", "http://localhost:8000")
    """Base URL of the FL Demonstrator server. Default: `http://localhost:8000`"""
    FL_DEMONSTRATOR_TRAINING_SCRIPT_EXECUTOR: str = environ.get("FL_DEMONSTRATOR_TRAINING_SCRIPT_EXECUTOR", "python")
    """Path to the script executor. Default: `python`"""
    FL_DEMONSTRATOR_TRAINING_SCRIPT_PATH: str = environ.get("FL_DEMONSTRATOR_TRAINING_SCRIPT_PATH", "src/main.py")
    """Path to the training script. Default: `src/main.py`"""
    FL_DEMONSTRATOR_TRAINING_WORKING_DIRETORY: str = environ.get("FL_DEMONSTRATOR_TRAINING_WORKING_DIRETORY", ".")
    """Working directory for the training script. Default: `.`"""

    SERVER_HOST: str = environ.get("FL_CLIENT_SERVER_HOST", "0.0.0.0")
    """Client server hostname. Default: `0.0.0.0`"""
    SERVER_PORT: int = int(environ.get("FL_CLIENT_SERVER_PORT", "8101"))
    """Client server port. Default: `8101`"""

    MAIN_MODULE: str = "dlr.fl.client.__main__.default_main"
    """Main entry point of the client server. Default: `dlr.fl.client.__main__.default_main`"""
    COMMUNICATION_MODULE: str = "dlr.fl.client.communication.Communication"
    """Communication module of the client. Default: `dlr.fl.client.communication.Communication`"""
