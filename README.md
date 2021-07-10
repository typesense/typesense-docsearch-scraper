# Typesense DocSearch scraper

This is a fork of Algolia's awesome [DocSearch Scraper](https://github.com/algolia/docsearch-scraper), customized to index data in [Typesense](https://typesense.org). 

You'd typically setup this scraper to run on your documentation site, and then use [typesense-docsearch.js](https://github.com/typesense/typesense-docsearch.js) to add a search bar to your site. 

## Usage

#### Step 1: Create a DocSearch Config File

Follow the official [DocSearch documentation](https://docsearch.algolia.com/docs/required-configuration/) to create a `config.json` file.

[This repo](https://github.com/algolia/docsearch-configs/tree/master/configs) contains several Docsearch configuration files used by different documentation sites and [here's](https://github.com/typesense/typesense-website/blob/master/docs-site/docsearch.config.js) Typesense Documentation Site's docsearch config.

You can also use one of those as templates to create your own `config.js`, pointing to your documentation site.

#### Step 2: Run the Scraper

The easiest way to run the scraper is using Docker.

1. [Install Docker](https://docs.docker.com/get-docker/)
2. [Install jq](https://stedolan.github.io/jq/download/)
3. [Run Typesense](https://typesense.org/docs/latest/guide/install-typesense.html)
4. Create a `.env` file with the following contents:
    ```
    TYPESENSE_API_KEY=xyz      # Replace with your Typesense admin key
    TYPESENSE_HOST=localhost   # Replace with your Typesense host
    TYPESENSE_PORT=8108        # Replace with the port you are running Typesense on (443 for Typesense Cloud)
    TYPESENSE_PROTOCOL=http    # Use https for production deployments (https for Typesense Cloud)
    ```
5. Run the scraper:
    ```shellsession
    docker run -it --env-file=/path/to/your/.env -e "CONFIG=$(cat /path/to/your/config.json | jq -r tostring)" typesense/docsearch-scraper
    ```

This will scrape your documentation site and index it into Typesense.

#### Step 3: Add typesense-docsearch.js to your documentation site

Head over to [typesense-docsearch.js](https://github.com/typesense/typesense-docsearch.js) for instructions on how to setup a search bar in your documentation site, that uses the data this scraper indexes into your Typesense cluster.

## Help

If you have any questions or run into any problems, please create a Github issue and we'll try our best to help.
