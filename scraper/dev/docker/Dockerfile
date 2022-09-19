FROM typesense/docsearch-scraper-base
LABEL maintainer="contact@typesense.org"

WORKDIR /home/seleuser
USER seleuser
COPY scraper/src ./src

ENTRYPOINT ["pipenv", "run", "python", "-m", "src.index"]
