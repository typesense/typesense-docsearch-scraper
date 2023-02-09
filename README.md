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
# Install dependencies for pyenv:
# https://github.com/pyenv/pyenv/wiki#suggested-build-environment
sudo apt update && sudo apt install \
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

# Reload the shell so that the pyenv is present.
bash

# Install Python 3.6 inside pyenv:
pyenv install 3.6

# Set Python 3.6 to be the active version:
pyenv local 3.6

# Upgrade pip:
pip install --upgrade pip

# Install pipenv:
pip install --user pipenv

# There will be a warning:
# "The script virtualenv-clone is installed in '/home/[username]/.local.bin' which is not on PATH."
# Fix the warning by adding it to the PATH:
echo >> ~/.bashrc
echo '# Fixing pipx warning' >> ~/.bashrc
echo 'PATH=$PATH:~/.local/bin' >> ~/.bashrc

# Reload the shell so that the variable is present.
bash

# Ensure that you are in the "typesense-docsearch-scraper" directory.
# Then, install the Python dependencies:
pipenv install

# Then, open a shell with with the Python environment:
pipenv shell
```

## Help

If you have any questions or run into any problems, please create a Github issue and we'll try our best to help.
