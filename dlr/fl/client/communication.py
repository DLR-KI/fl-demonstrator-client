# SPDX-FileCopyrightText: 2024 Benedikt Franke <benedikt.franke@dlr.de>
# SPDX-FileCopyrightText: 2024 Florian Heinrich <florian.heinrich@dlr.de>
#
# SPDX-License-Identifier: Apache-2.0

import base64
from io import BytesIO
import logging
import requests
from subprocess import Popen
import torch
from typing import Any, Dict, Type, TypeVar
from uuid import UUID
import warnings

from .exceptions import MetricsUploadException, ModelDownloadException, ModelUploadException


T = TypeVar("T", bound="Communication")


def is_torchscript_instance(obj: Any) -> bool:
    return isinstance(obj, torch.jit.ScriptModule | torch.jit.ScriptFunction)


class Communication:
    """
    Client communication module.

    This module is responsible for the communication between the server and the client training/testing/etc. scripts.
    """

    _logger = logging.getLogger("fl.client")

    def __init__(
        self,
        client_id: UUID,
        training_id: UUID,
        round: int,
        model_id: UUID,
        http_authorization: str,
    ) -> None:
        """
        Create a new client communication module instance.

        Args:
            client_id (UUID): UUID of the client
            training_id (UUID): UUID of the training
            round (int): number of the training round
            model_id (UUID): UUID of the global model
            http_authorization (str): HTTP authorization header value
        """
        self.client_id = client_id
        """UUID of the client."""
        self.training_id = training_id
        """UUID of the training."""
        self.round = round
        """Number of the training round."""
        self.model_id = model_id
        """UUID of the global model."""
        self.http_authorization = http_authorization
        """HTTP authorization header value."""

    @classmethod
    def from_user_password(
        cls: Type[T],
        client_id: UUID, training_id: UUID, round: int, model_id: UUID,
        username: str, password: str
    ) -> T:
        """
        Create a new client communication module instance from a username and password.

        Args:
            client_id (UUID): UUID of the client
            training_id (UUID): UUID of the training
            round (int): number of the training round
            model_id (UUID): UUID of the global model
            username (str): Authorization username
            password (str): Authorization password

        Returns:
            T: new client communication module instance
        """
        return cls(
            client_id, training_id, round, model_id,
            "Basic " + base64.b64encode(
                f"{username}:{password}".encode("utf-8")  # noqa: E231
            ).decode("utf-8")
        )

    @classmethod
    def from_http_authorization(
        cls: Type[T],
        client_id: UUID, training_id: UUID, round: int, model_id: UUID,
        http_authorization: str
    ) -> T:
        """
        Create a new client communication module instance from a HTTP authorization header value.

        Args:
            client_id (UUID): UUID of the client
            training_id (UUID): UUID of the training
            round (int): number of the training round
            model_id (UUID): UUID of the global model
            http_authorization (str): HTTP authorization header value

        Returns:
            T: new client communication module instance
        """
        return cls(client_id, training_id, round, model_id, http_authorization)

    ###################################################################################################################
    # Server calls

    @classmethod
    def _start_script(cls: Type[T], action: str, training_id: UUID, round: int, model_id: UUID) -> None:
        """
        Start the trainings script to train the next round.

        The script gets a positional argument (`train` or `test`) as well as the training id (`--training-id`),
        the round number (`--round`) and the model id (`--model-id`) as arguments.
        The script start can be configured in the `Settings` module over the attributes:

        - `FL_DEMONSTRATOR_TRAINING_SCRIPT_EXECUTOR`: path to the script executor (e.g. `python3`)
        - `FL_DEMONSTRATOR_TRAINING_SCRIPT_PATH`: path to the training script
        - `FL_DEMONSTRATOR_TRAINING_WORKING_DIRETORY`: working directory for the training script

        Args:
            action (str): positional argument/action to perform (`train` or `test`)
            training_id (UUID): UUID of the training
            round (int): number of the training round
            model_id (UUID): UUID of the global model
        """
        from . import Settings
        args = [
            action,
            "--training-id", str(training_id),
            "--round", str(round),
            "--model-id", str(model_id),
        ]
        cls._logger.debug(args)
        Popen(
            [Settings.FL_DEMONSTRATOR_TRAINING_SCRIPT_EXECUTOR, Settings.FL_DEMONSTRATOR_TRAINING_SCRIPT_PATH] + args,
            cwd=Settings.FL_DEMONSTRATOR_TRAINING_WORKING_DIRETORY
        )

    @classmethod
    def start_training(cls: Type[T], training_id: UUID, round: int, model_id: UUID) -> None:
        """
        Start the trainings script to train the next round.

        Also see documentation of `_start_script`.

        Args:
            training_id (UUID): UUID of the training
            round (int): number of the training round
            model_id (UUID): UUID of the global model
        """
        cls._logger.info("training start")
        cls._start_script("train", training_id, round, model_id)

    @classmethod
    def start_testing(cls: Type[T], training_id: UUID, round: int, model_id: UUID) -> None:
        """
        Start the trainings script to test the current global model.

        Also see documentation of `_start_script`.

        Args:
            training_id (UUID): UUID of the training
            round (int): number of the training round
            model_id (UUID): UUID of the global model
        """
        cls._logger.info("testing start")
        cls._start_script("test", training_id, round, model_id)

    @classmethod
    def init_training(cls: Type[T], training_id: UUID, model_id: UUID) -> None:
        """
        Start the initialization training procedure of the client.

        Args:
            training_id (UUID): UUID of the training
            model_id (UUID): UUID of the global model
        """
        cls._logger.info("training init")
        print("Training is initialized.")

    @classmethod
    def end_training(cls: Type[T], training_id: UUID, model_id: UUID) -> None:
        """
        Start the end training procedure of the client.
        I.e. clean up and shutdown the client for the specific training.

        Args:
            training_id (UUID): UUID of the training
            model_id (UUID): UUID of the global model
        """
        cls._logger.info("training end")
        print("Training is finished. Start clean up und shutdown :D")

    @classmethod
    def unknown_message(cls: Type[T], mesage_type: str, training_id: UUID, data: Any) -> int:
        """
        Handle an unknown notification from the server.

        Args:
            training_id (UUID): UUID of the training
            model_id (UUID): UUID of the global model
            data (Any): notification body

        Returns:
            int: http response status code
        """
        cls._logger.warn("unknown server message")
        print(f"Known message. Ignore message of type: {mesage_type}")
        return 400

    ###################################################################################################################
    # client calls

    def download_model(self) -> Any:
        """
        Download the global model from the server.

        Raises:
            ModelDownloadException: Model download failed

        Returns:
            Any: global model
        """
        from . import Settings
        self._logger.info("model download")
        response = requests.get(
            Settings.FL_DEMONSTRATOR_BASE_URL + f"/api/models/{self.model_id}/",
            headers=self.get_headers()
        )
        if response.status_code != 200:
            self._logger.error(f"model download response with status code: {response.status_code}")
            raise ModelDownloadException(response)
        return self.unpack_model(response.content)

    def upload_model(self, model: Any, metrics: Dict[str, Any], sample_size: int) -> bool:
        """
        Upload the local model to the server including the metrics and the sample size.

        Args:
            model (Any): local model
            metrics (Dict[str, Any]): metrics of the local model
            sample_size (int): sample size of the training data

        Raises:
            ModelUploadException: Model upload failed

        Returns:
            bool: `True` if model upload was successful; otherwise `False`
        """
        from . import Settings
        self._logger.info("model upload")
        response = requests.post(
            Settings.FL_DEMONSTRATOR_BASE_URL + f"/api/models/{self.model_id}/",
            data={
                "owner": self.client_id,
                "round": self.round,
                "sample_size": sample_size,
                "metric_names": list(metrics.keys()),
                "metric_values": list(metrics.values()),
            },
            files={
                "model_file": self.pack_model(model),
            },
            headers=self.get_headers()
        )
        if response.status_code != 201:
            self._logger.error(f"model upload response with status code: {response.status_code}")
            raise ModelUploadException(response)
        return True

    def upload_metrics(self, metrics: Dict[str, Any]) -> bool:
        """
        Upload the global model metrics to the server.

        Args:
            metrics (Dict[str, Any]): metrics of the local model

        Raises:
            MetricsUploadException: Metrics upload failed

        Returns:
            bool: `True` if metrics upload was successful; otherwise `False`
        """
        from . import Settings
        self._logger.info("metrics upload")
        response = requests.post(
            Settings.FL_DEMONSTRATOR_BASE_URL + f"/api/models/{self.model_id}/metrics/",
            data={
                "metric_names": list(metrics.keys()),
                "metric_values": list(metrics.values()),
            },
            headers=self.get_headers()
        )
        if response.status_code != 201:
            self._logger.error(f"model metrics upload response with status code: {response.status_code}")
            raise MetricsUploadException(response)
        return True

    ###################################################################################################################
    # helper methods

    def get_headers(self) -> Dict[str, str]:
        """
        Get default HTTP headers for the communication with the server.

        Returns:
            Dict[str, str]: HTTP headers as key-value pairs
        """
        return {
            "Authorization": self.http_authorization,
        }

    def unpack_model(self, blob: bytes) -> Any:
        """
        Unpack a model from a blob.

        Args:
            blob (bytes): data blob to unpack

        Returns:
            Any: unpack model
        """
        # torch.load support torch.nn.Module as well as torchscript (but with user warning)
        with warnings.catch_warnings():
            warnings.filterwarnings(
                "ignore",
                message="'torch.load' received a zip file that looks like a TorchScript archive",
                category=UserWarning
            )
            return torch.load(BytesIO(blob))

    def pack_model(self, model: Any) -> bytes:
        """
        Pack a model to a blob.

        Args:
            model (Any): data (model) to pack

        Returns:
            bytes: data blob
        """
        buffer = BytesIO()
        if is_torchscript_instance(model):
            self._logger.debug("save torchscript model")
            torch.jit.save(model, buffer)
        else:
            self._logger.debug("save torch model")
            torch.save(model, buffer)
        return buffer.getvalue()
