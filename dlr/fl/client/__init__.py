# SPDX-FileCopyrightText: 2024 Benedikt Franke <benedikt.franke@dlr.de>
# SPDX-FileCopyrightText: 2024 Florian Heinrich <florian.heinrich@dlr.de>
#
# SPDX-License-Identifier: Apache-2.0

from importlib import import_module
from os import environ
import sys
from typing import Any, Type

from .settings import Settings as SettingsBase
from .communication import Communication as CommunicationBase


# fix import issues when running training and import custom settings module
for path in environ.get("FL_CLIENT_ADDITIONAL_SYS_PATH", "").split(":"):
    sys.path.append(path)


def import_string(dotted_path: str) -> Any:
    """
    Import a dotted module path and return the attribute/class designated by the
    last name in the path. Raise ImportError if the import failed.

    Args:
        dotted_path (str): The dotted path to the attribute/class/method to import.

    Returns:
        The attribute/class/method designated by the dotted path.

    Source: https://github.com/django/django/blob/01c00dc/django/utils/module_loading.py#L15-L33
    """
    try:
        module_path, class_name = dotted_path.rsplit('.', 1)
    except ValueError:
        msg = f"{dotted_path} doesn't look like a module path"
        raise ImportError(msg).with_traceback(sys.exc_info()[2])

    module = import_module(module_path)

    try:
        return getattr(module, class_name)
    except AttributeError:
        msg = f'Module "{dotted_path}" does not define a "{class_name}" attribute/class/method'
        raise ImportError(msg).with_traceback(sys.exc_info()[2])


Settings: Type[SettingsBase] = import_string(
    environ.get("FL_CLIENT_SETTINGS_MODULE", "dlr.fl.client.settings.Settings")
)
"""
Client settings module.

The client settings can be customized by creating a custom settings module and setting the environment variable
`FL_CLIENT_SETTINGS_MODULE` to the dotted path of the module.
By default and fallback the settings are loaded from the module `dlr.fl.client.settings.Settings`.
"""

Communication: Type[CommunicationBase] = import_string(
    Settings.COMMUNICATION_MODULE
    if hasattr(Settings, "COMMUNICATION_MODULE")
    else "dlr.fl.client.communication.Communication"
)
"""
Client communication module.

The client communication can be customized by setting the `COMMUNICATION_MODULE` attribute inside the Settings
to the dotted path of the module.
By default and fallback the communication is loaded from the module
`dlr.fl.client.communication.Communication`.
"""


__all__ = ["Settings", "Communication"]
