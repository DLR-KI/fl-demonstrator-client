FROM python:3.10-slim

# add user: client
RUN useradd -ms /bin/bash client
USER client
WORKDIR /home/client/app

# install app
COPY --chown=client:client pyproject.toml README.md /home/client/app/
RUN mkdir -p dlr/fl/client && \
    pip install --no-warn-script-location . && \
    rm -rf dlr pyproject.toml README.md

STOPSIGNAL SIGKILL
EXPOSE 8101
CMD ["python", "-m", "dlr.fl.client"]
