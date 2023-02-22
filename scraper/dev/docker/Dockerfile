FROM typesense/docsearch-scraper-base:0.3.5
LABEL maintainer="contact@typesense.org"

WORKDIR /root
COPY scraper/src ./src

ENTRYPOINT ["pipenv", "run", "python", "-m", "src.index"]
