# Getting Started

Step 1: Download additional tools

The Omega Assertion Framework (OAF) requires a few tools to run properly:

* Python
* OpenPolicyAgent
* jq
* Docker
* OpenSSL

Make sure these are all available and on your path.

Step 2: Create a key pair

This is just for basic testing - we expect to remove this entirely in favor of
signatures at a higher level.

```
openssl ecparam -name prime256v1 -genkey -noout -out private-key.pem
openssl ec -in private-key.pem -pubout -out public-key.pem
```

Step 2: Initialize the Python virtual environment

```
python -mvenv venv
source venv/bin/activate (or .\venv\Scripts\activate.ps1 on Windows)
pip install -r requirements.txt
```

Step 2: Create an assertion

```
python create-assertion.py \
    --assertion ManualSecurityReview \
    --package-url pkg:npm/left-pad@1.3.0 \
    --assertion_pass true \
    --review_text 'This was a lot of fun.' \
    --private-key private-key.pem | tee left-pad-assertion.json
```

Step 3: Check the assertion with policy

```
./check_policy.sh left-pad-assertion.json recent_security_review
```

Here, `recent_security_review` refers to `assertions/policies/recent_security_review.rego`,
which defines the logic for what "pass" means.

# Contributing

Since OAF is so new, we don't really need lots of policies or assertions generated,
but a few more to iron out the wrinkles and address cases that we haven't seen would
be interesting.

There are definitely missing important features (like validating a signature --
deferred out since we expect to be using a higher-level standard for this) and a more
pleasing UX.

We also need to think about where to store these assertions so they can be looked up
quickly.