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

Step 2: Create an assertion

```
python .\create-assertion.py
    --assertion ManualReviewAssertion
    --package-url pkg:npm/left-pad@1.3.0
    --assertion_pass true
    --review_text 'This was a lot of fun.'
    --private-key .\private-key.pem
    --input_file ..\results\npm\left-pad\1.3.0\reference-binaries\npm-left-pad@1.3.0.tgz

