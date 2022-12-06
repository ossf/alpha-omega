# Getting Started

This document describes how to get started with OAF, in terms of setting
up a system with the proper tools and configuration.

First, we're only currently testing OAF on Linux. There isn't anything that
can't work on Windows, but various scripts make assumptions on things like
path separators.  Pull requests to improve support here are more welcome.

OAF *should* work within a WSL environment, as long as the underlying tools
are available.

Step 1: Download additional tools

The Omega Assertion Framework (OAF) requires a few tools to run properly:

* [Python 3](https://python.org)
* [OpenPolicyAgent](https://openpolicyagent.org)
* [Docker](https://docker.com)

Technically, OpenPolicyAgent is only required for consuming (evaluating)
assertions, and Docker is only required for generating them.

If you want to use key pair signing, you'll also need to provide or create
a key pair, and OpenSSL can be used for this.

Make sure all tools are available on your path.

Step 2: Create a key pair (optional)

```
openssl ecparam -name prime256v1 -genkey -noout -out private-key.pem
openssl ec -in private-key.pem -pubout -out public-key.pem
```

Step 2: Initialize the Python virtual environment

The Python virtual environment uses a requirements.txt file provided.
```
python -mvenv venv
source venv/bin/activate
pip install -r requirements.txt
```

If you intend to contribute to OAF, you might want to also install
requirements from `dev-requirements.txt`, which include a few linters.

Step 3: Generate assertions

```
mkdir output
python analyze.py --package-url=pkg:npm/left-pad@1.3.0 --repository=dir:$(pwd)/output
```

Step 4: Run policies against assertions

```
python oaf.py consume --subject=pkg:npm/left-pad@1.3.0 --repository=dir:$(pwd)/output
```
