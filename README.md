# Typesense DocSearch scraper

This is a fork of Algolia's awesome [DocSearch Scraper](https://github.com/algolia/docsearch-scraper), customized to index data in [Typesense](https://typesense.org). 

You'd typically setup this scraper to run on your documentation site, and then use [typesense-docsearch.js](https://github.com/typesense/typesense-docsearch.js) to add a search bar to your site. 

#### What is Typesense? 

If you're new to Typesense, it is an **open source** search engine that is simple to use, run and scale, with clean APIs and documentation. 

Think of it as an open source alternative to Algolia and an easier-to-use, batteries-included alternative to ElasticSearch. Get a quick overview from [this guide](https://typesense.org/guide/).

## Usage

Read detailed step-by-step instructions on how to configure and setup the scraper on Typesense's dedicated documentation site: https://typesense.org/docs/latest/guide/docsearch.html

## Compatibility

| typesense-docsearch-scraper | typesense-server |
| --- | --- |
| 0.5.0 | >= 0.22.1 |
| 0.4.x and below | >= 0.21.0  |

## Tips for more complex use-cases

The official guide explains to create a `.env` file with the following contents:

```
TYPESENSE_API_KEY=xyz
TYPESENSE_HOST=xxx.a1.typesense.net
TYPESENSE_PORT=443
TYPESENSE_PROTOCOL=https
```

And then run the following command to start the scraper:

```
docker run -it \
  --env-file=/path/to/your/.env  \
  -e "CONFIG=$(cat config.json | jq -r tostring)" \
  typesense/docsearch-scraper
```

This will work for most simple setups.  However, there's a
few common challenges that are not addressed by this example, so below are some
pointers for those with more complicated use-cases:

### Trusting certificates from internal CAs

If you're trying to scrape a website that is secured with a certificate from an
internal CA -- common for corporate intranets for example -- , you will need to
somehow make the container trust this CA. To do so, you can mount a file
with trusted CAs and then pass it as a command line option.

In the example below, a file in the current folder names `ca-chain.crt` will be added to the trusted CA list:

```
docker run -it \
  --mount type=bind,source="$(pwd)/ca-chain.crt",target=/etc/ssl/certs/ca-certificates.crt \
  --env "REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt" \
  --env-file=/path/to/your/.env  \
  -e "CONFIG=$(cat config.json | jq -r tostring)" \
  typesense/docsearch-scraper
```

### Passing a config file location, rather than a config string

The official example uses the `jq` tool to parse the config file into a JSON string prior to passing it as the `CONFIG` environment variable.

If you don't have `jq` available, it's good to know that you can also pass the location of the config file to the `CONFIG` variable, and then the file will be read from this location.

Just make sure that the config is available inside the container. In other words, you'll need to voume mount it, like in the example below:

```
docker run -it \
  -v "/path/to/config/dir/on/your/machine:/tmp/search" \
  -e "CONFIG=/tmp/search/typesense.json" \
  typesense/docsearch-scraper
```

### Set environment variables on the command line, rather than using a .env file

If you don't want to use a `.env` file or cannot use one in your setup, you can also pass all variables on the command line:

```
docker run -it \
  -e "TYPESENSE_API_KEY=xyz" \
  -e "TYPESENSE_HOST=xxx.a1.typesense.net" \
  -e "TYPESENSE_PORT=443" \
  -e "TYPESENSE_PROTOCOL=https" \
  -e "CONFIG=$(cat config.json | jq -r tostring)" \
  typesense/docsearch-scraper
```

### Resolving hosts

If your scraper depends on host resolution that is not available inside the container, you can add a host entry on the command line:

```
docker run -it \
  --add-host intranet.company.com:10.1.2.3 \
  --env-file=/path/to/your/.env  \
  -e "CONFIG=$(cat config.json | jq -r tostring)" \
  typesense/docsearch-scraper
```

### Authentication

If you're looking to scrape content that requires authentication, there's a
number of options that are supported out of the box:


#### Cloudflare Zero Trust (CF)

To use this authentication, set these environment variables:

- `CF_ACCESS_CLIENT_ID`
- `CF_ACCESS_CLIENT_SECRET`

#### Google Identity-Aware Proxy (IAP)

To use this authentication, set these environment variables:

- `IAP_AUTH_CLIENT_ID`
- `IAP_AUTH_SERVICE_ACCOUNT_JSON`

#### Keycloak (KC)

To use this authentication, set these environment variables:

- `KC_URL`
- `KC_REALM`
- `KC_CLIENT_ID`
- `KC_CLIENT_SECRET`

## Development Workflow

This section only applies if you're making changes to this scraper itself. If you only need to run the scraper, see Usage instructions above.

#### Releasing a new version

Basic/abbreviated instructions:

```shellsession
$ pipenv shell
$ ./docsearch docker:build
$ git tag -a 0.2.1 -m "0.2.1"
$ ./docsearch deploy:scraper
$ git push --follow-tags
```

Detailed instructions starting from a fresh Ubuntu Server 22.02:

```bash
# Install Docker:
# https://docs.docker.com/engine/install/ubuntu/
sudo apt update
sudo apt remove docker docker-engine docker.io containerd runc --yes
sudo apt install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release \
    --yes
sudo mkdir -m 0755 -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install \
  docker-ce \
  docker-ce-cli \
  containerd.io \
  docker-buildx-plugin \
  docker-compose-plugin \
  --yes
sudo docker run hello-world

# Run Docker as a non-root user:
# https://www.digitalocean.com/community/questions/how-to-fix-docker-got-permission-denied-while-trying-to-connect-to-the-docker-daemon-socket
sudo usermod -aG docker ${USER}
exit
# (Relogin.)
docker run hello-world

# Install dependencies for pyenv:
# https://github.com/pyenv/pyenv/wiki#suggested-build-environment
sudo apt update
sudo apt install \
  build-essential \
  curl \
  libbz2-dev \
  libffi-dev \
  liblzma-dev \
  libncursesw5-dev \
  libreadline-dev \
  libsqlite3-dev \
  libssl-dev \
  libxml2-dev \
  libxmlsec1-dev \
  llvm \
  make \
  tk-dev \
  wget \
  xz-utils \
  zlib1g-dev \
  --yes

# Install pyenv:
# https://github.com/pyenv/pyenv#automatic-installer
curl https://pyenv.run | bash

# Add pyenv to path:
echo >> ~/.bashrc
echo '# Adding pyenv' >> ~/.bashrc
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
source ~/.bashrc

# Install Python 3.10 inside pyenv:
pyenv install 3.10

# Set the active version of Python:
pyenv local 3.10

# Upgrade pip:
pip install --upgrade pip

# Install pipenv:
pip install --user pipenv

# There will be a warning:
# "The script virtualenv-clone is installed in '/home/[username]/.local.bin' which is not on PATH."
# Fix the warning by adding it to the PATH:
echo >> ~/.bashrc
echo '# Fixing pip warning' >> ~/.bashrc
echo 'PATH=$PATH:~/.local/bin' >> ~/.bashrc
source ~/.bashrc

# Ensure that you are in the "typesense-docsearch-scraper" directory.
# Then, install the Python dependencies for this project:
pipenv --python 3.10
pipenv lock --clear
pipenv install

# Then, open a shell with with the Python environment:
pipenv shell

# Build a new version of the Docker container.
export TAG="0.4.1"
docker buildx build -f ./scraper/dev/docker/Dockerfile -t typesense/docsearch-scraper:${TAG} .
docker push typesense/docsearch-scraper:${TAG}
docker tag typesense/docsearch-scraper:${TAG} typesense/docsearch-scraper:latest
docker push typesense/docsearch-scraper:latest

# Add a new Git tag.
git tag -a "$TAG" -m "$TAG"

# Sync with GitHub.
git push --follow-tags
```

## Help

If you have any questions or run into any problems, please create a Github issue and we'll try our best to help.
