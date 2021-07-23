# Typesense DocSearch scraper

This is a fork of Algolia's awesome [DocSearch Scraper](https://github.com/algolia/docsearch-scraper), customized to index data in [Typesense](https://typesense.org). 

You'd typically setup this scraper to run on your documentation site, and then use [typesense-docsearch.js](https://github.com/typesense/typesense-docsearch.js) to add a search bar to your site. 

#### What is Typesense? 

If you're new to Typesense, it is an **open source** search engine that is simple to use, run and scale, with clean APIs and documentation. 

Think of it as an open source alternative to Algolia and an easier-to-use, batteries-included alternative to ElasticSearch. Get a quick overview from [this guide](https://typesense.org/guide/).

## Usage

Read detailed step-by-step instructions on how to configure and setup the scraper on Typesense's dedicated documentation site: https://typesense.org/docs/latest/guide/docsearch.html

## Development Workflow

This section only applies if you're making changes to this scraper itself. If you only need to run the scraper, see Usage instructions above.

#### Releasing a new version

```shellsession
$ pipenv shell
$ ./docsearch docker:build
$ git tag -a 0.2.1 -m "0.2.1"
$ ./docsearch deploy:scraper
$ git push --follow-tags

```

## Help

If you have any questions or run into any problems, please create a Github issue and we'll try our best to help.
