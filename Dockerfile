FROM ghcr.io/autsunset/epic-free@sha256:eb786036b469823388cd673785caeb5dbfe6bd9ff594f8ebf86eeab49f3db5e8
WORKDIR /opt/epic-helper
COPY upstream/pyproject.toml upstream/uv.lock ./
RUN uv sync --frozen --no-dev --python 3.12
COPY upstream/app/ ./app/
COPY run.py login_compat.py claim_guard.py worker.py /adapter/
ENV PYTHONPATH=/opt/epic-helper/app:/adapter
ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["/opt/epic-helper/.venv/bin/python", "/adapter/run.py", "claim"]
