FROM debian:bookworm-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        bash \
        ca-certificates \
        findutils \
        git \
        gh \
        tzdata \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

COPY docker/auto_sync_runner.sh /usr/local/bin/auto_sync_runner.sh
RUN chmod +x /usr/local/bin/auto_sync_runner.sh

CMD ["/usr/local/bin/auto_sync_runner.sh"]