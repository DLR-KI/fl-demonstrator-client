#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler
import json
import logging
from typing import Any
from uuid import UUID

from . import Communication


class ClientServerHandler(BaseHTTPRequestHandler):
    """
    Default client server handler.

    The handler will receive notifications from the server and forward them to the client communication module.
    """

    _logger = logging.getLogger("fl.client")
    """Logger instance for the client server handler."""

    def do_POST(self):
        """
        Receive a notification from the server.

        All notifications are expected to be in JSON format and contain the following fields:

        - `notification_type`: The type of the notification.
        - `training_uuid`: The UUID of the corresponding training.
        - `body`: The notification body.

        If an error occurs during the handling of the notification, the error will be logged
        and a 500 response is sent.
        """
        try:
            content_len = int(self.headers.get("Content-Length"))
            request_content = self.rfile.read(content_len)
            content = json.loads(request_content)
            self._logger.debug("notification received: " + json.dumps(content))
            self.handle_message(
                str(content["notification_type"]),
                UUID(content["training_uuid"]),
                content["body"],
            )
        except Exception as e:
            self._logger.fatal(e)
            self.send_response(500)
        self.end_headers()

    def handle_message(self, notification_type: str, training_id: UUID, data: Any):
        """
        Forward the notification to the corresponding client communication module function.

        Args:
            notification_type (str): type of the notification
            training_id (UUID): UUID of the corresponding training
            data (Any): notification body
        """
        self._logger.info(f"receive notification '{notification_type}' for training '{training_id}'")
        match notification_type:
            case "TRAINING_START":
                Communication.init_training(
                    training_id=training_id,
                    model_id=UUID(data["global_model_uuid"]),
                )
                self.send_response(200)
            case "UPDATE_ROUND_START":
                Communication.start_training(
                    training_id=training_id,
                    round=int(data["round"]),
                    model_id=UUID(data["global_model_uuid"]),
                )
                self.send_response(202)
            case "MODEL_TEST_ROUND":
                Communication.start_testing(
                    training_id=training_id,
                    round=int(data["round"]),
                    model_id=UUID(data["global_model_uuid"]),
                )
                self.send_response(202)
            case "TRAINING_FINISHED":
                Communication.end_training(
                    training_id=training_id,
                    model_id=UUID(data["global_model_uuid"]),
                )
                self.send_response(200)
            case _:
                status_code = Communication.unknown_message(
                    mesage_type=data["notification_type"],
                    training_id=training_id,
                    data=data["data"],
                )
                self.send_response(status_code)
