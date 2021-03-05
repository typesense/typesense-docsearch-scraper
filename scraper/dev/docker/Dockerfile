FROM typesense/docsearch-scraper-base
LABEL maintainer="contact@typesense.org"

WORKDIR /root
COPY scraper/src ./src

ENTRYPOINT ["pipenv", "run", "python", "-m", "src.index"]
