FROM python:3.12

ENV DEBIAN_FRONTEND=noninteractive
ENV POETRY_VIRTUALENVS_IN_PROJECT=1

RUN apt update && \
    apt install -y --no-install-recommends neovim mediainfo && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN pip install poetry && \
    poetry install --without dev --no-root && \
    rm -rf ~/.cache/

COPY sachi sachi
COPY README.md .
RUN poetry install --only-root

ENV EDITOR=nvim
ENTRYPOINT [ "poetry", "run", "python3", "-m", "sachi" ]
VOLUME [ "/root/.config/sachi" ]
