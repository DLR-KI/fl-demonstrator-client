# SPDX-FileCopyrightText: 2024 Benedikt Franke <benedikt.franke@dlr.de>
# SPDX-FileCopyrightText: 2024 Florian Heinrich <florian.heinrich@dlr.de>
#
# SPDX-License-Identifier: Apache-2.0

FROM python:3.10-slim

# add user: client
RUN useradd -ms /bin/bash client
USER client
RUN mkdir /home/client/app
WORKDIR /home/client/app

# install app dependencies (only)
COPY --chown=client:client pyproject.toml README.md /home/client/app/
RUN mkdir -p dlr/fl/client && \
    pip install --no-warn-script-location . && \
    rm -rf dlr

# install app
COPY --chown=client:client dlr /home/client/app/dlr
RUN pip install --no-warn-script-location . && \
    rm -rf pyproject.toml README.md

STOPSIGNAL SIGKILL
EXPOSE 8101
CMD ["python", "-m", "dlr.fl.client"]
