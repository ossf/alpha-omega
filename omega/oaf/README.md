# Omega Assertion Framework

The Omega Assertion Framework (OAF) is a series of tools for generating assertions reflecting facts
about a subject, and for consuming those assertions through policies.

OAF was designed to allow organizations to make decisions based on the security quality of open
source projects through a rich, flexible, but simple data set.

## Project Status

OAF is highly experimental, and should not be relied upon for anything important. We encourage
others to try it out, [submit feedback](https://github.com/ossf/alpha-omega/issues), and contribute
ideas or code, but we may change any part of this radically at any time.

We hope for the project to be slightly more mature and controlled in early 2023.

### Contributing

If you'd like to contribute, please get in touch with us via an issue or on the OpenSSF
[#alpha_omega](https://openssf.slack.com/archives/C02LUUWQZNK) Slack. Pull requests are welcome.

## Getting Started

### Preliminaries

In order to use OAF properly, you'll need to install a few tools, set up a Python virtual
environment, and gather a few environment variables. Instructions on this can be found in the
[getting-started](doc/getting-started.md) doc.

### Generating Assertions

To get started, we have a simple runner that you can use to generate some assertions.

```
mkdir output
python analyze.py --package-url pkg:npm/left-pad@1.3.0 --repository dir:$(pwd)/output
```

The `analyze.py` calls `oaf.py` multiple times, once to create each assertion, with some sensible
defaults. After a few minutes, you should see a series of files in `output`, each one representing
one assertion.

### Consuming Assertions

To consume assertions, you can use the `oaf.py` entrypoint directly:

```
python oaf.py consume --subject=pkg:npm/left-pad@1.3.0 --repository=dir:$(pwd)/output
```

You should see JSON output representing the execution of the built-in policies against the
assertions you generated above.

For example, part of that output should look like:

```
  {
    "policy_name": "process.is_latest_version",
    "execution_result": {
      "state": "pass",
      "message": "true"
    }
  }

```

This means the `is_latest_version` policy was executed and passed, so `pkg:npm/left-pad@1.3.0` is
indeed the latest version of the package.

### Exploring Built-In Assertions & Policies

All of the assertions types are located in the
[omega/assertion/assertion](omega/assertion/assertion) directory. Some assertions perform
processing (like `SecurityAdvisory`, which calls the https://deps.dev endpoint to retrieve
known vulnerabilities), while others require an input (like `Language`, which uses the output
of [Application Inspector](https://github.com/Microsoft/ApplicationInspector).

All policies are located in the [omega/assertion/policy](omega/assertion/policy/) directory, and
more specifically, within [builtin](omega/assertion/policy/builtin/) or
[samples](omega/assertion/policy/samples/).

## Assertions

Assertions are "facts" about a subject, such as, "The weather in Washington was rainy yesterday."
Assertions could also be called "claims".

All OAF-compatible assertions have three key fields:

* **subject**: This is the target of the assertion -- the "thing" that the assertion is referring
  to. Since there are various different types of subjects, including packages, projects,
  or repositories, the subject itself contains two fields, a `type`, which is a URI that expresses
  the type of the subject, and one or more other fields that expresses the subject.

* **predicateType**: This is a URI that expresses the structure of the predicate, and varies based
  on the predicate. For example, the `SecurityAdvisory` assertion uses a predicateType of
  `https://github.com/ossf/alpha-omega/security_advisories/0.1.0`. In the future, this will likely
  refer to an actual schema definition, but for now, it should be treated as an opaque identifier,
  with a definition evident from the content produced. (This statement is as unsatisfying for us
  as it is for you -- it'll get better.)

* **predicate**: This is the part of the predicate that contains the interesting content. It's
  structure is tied to the `predicateType`.

Within the predicate, most (possibly all) assertions will share a similar sub-structure:

* **content**: This is the raw, inner-most core of what the assertion is saying, and is very
  much assertion-dependent.

* **evidence**: This is typically evidence provided for transparency, and could be included
  directly as content or as a URL to remote evidence stored elsewhere. It may include a
  `reproducibility` field, which expresses the author's estimate of how likely the same evidence
  could be reproduced in the future.

* **generator**: This is a reference to the implementation that actually generated the assertion,
  and can be important when multiple tools (or versions of tools) could be used to generate the
  same logical assertion.

* **operational**: This field contains operational data, such as a system that the assertion
  was generated on, how long it took to generate it, and other such metadata. It's unclear whether
  this information provides any value, and may be removed in the future. This field also contains
  an `expiration` field, which can be used for assertions that are expected to have a limited
  lifetime of usefulness. It's also likely that this field will move to somewhere else in the
  assertion.

### Example Assertion

An example assertion might look like:

```
{
  "_type": "https://in-toto.io/Statement/v0.1",
  "predicate": {
    "content": {
      "metadata": {
        "is_latest_version": true,
        "latest_version": "1.3.0",
        "latest_version_deprecated": true,
        "latest_version_publish_date": "2018-04-09T01:10:45.796000+00:00",
        "version_deprecated": true,
        "version_publish_date": "2018-04-09T01:10:45.796000+00:00"
      }
    },
    "evidence": {
      "_type": "https://github.com/ossf/alpha-omega/types/evidence/file/v0.1",
      "content": {
        "output": "..."
      },
      "filename": "/tmp/omega-fbnxlnky/npm/left-pad/1.3.0/tool-metadata-native.json",
      "reproducibility": "high"
    },
    "generator": {
      "name": "openssf.omega.metadata",
      "version": "0.1.0"
    },
    "operational": {
      "environment": {
        "hostname": "scovetta-xps",
        "machine_identifier": "00000000-0000-0000-0000-cc96e5042f66"
      },
      "execution_start": "2022-11-30T20:49:14.257658Z",
      "execution_stop": "2022-11-30T20:49:14.258175Z",
      "expiration": "2024-11-29T20:49:14.192610Z",
      "timestamp": "2022-11-30T20:49:14.257656Z",
      "uuid": "4f3df5c0-2752-4daa-b426-87e35c0ed574"
    }
  },
  "predicateType": "https://github.com/ossf/alpha-omega/metadata/0.1.0",
  "subject": {
    "purl": "pkg:npm/left-pad@1.3.0",
    "type": "https://github.com/ossf/alpha-omega/subject/package_url/v0.1"
  }
}

```

## Signing

First, we know that the way we're approaching signing is wrong. We're going to change it to
something that makes a lot more sense, very likely be wrapping the assertion itself in a higher-
level construct, possibly [in-toto attestations](https://github.com/in-toto/attestation) or a
[SCITT envelope](https://datatracker.ietf.org/wg/scitt/about/). While we investigate, we'll
continue to provide a very basic signing capability, based on public/private keys.

If you provide a `--signer=<FILE>` parameter during assertion generation, that `<FILE>` should
be an RSA or EC private key, in which case it will be used to sign the assertion. If you pass
its corresponding public key in the same way during assertion evaluation, then the public
key will be used to validate the assertions.

## Repositories

A repository is a location where assertions can be stored and retrieved. There are no limitations
on the types of repositories used, but the reference implementation of OAF supports three:

* **Local file system**: If you use the `--repository=dir:<DIRECTORY>` parameter, then assertions
  will be stored or retrieved from a subdirectory within the directory provided.
* **SQLite database**: If you use the `--repository=sqlite:<FILE>` parameter, then the assertions
  will be stored or retrieved from the SQLite database provided. If the file does not exist, then
  a new file will be created an initialized with the proper table structure.
* **Neo4j database**: If you use the `--repository=neo4j<URI>` parameter, then the assertions
  will be stored or retrieved from a [Neo4j](https://neo4j.com) database. You'll need to provide
  a URI compatible with [py2neo](https://py2neo.org/2021.1/).
* **Simple Web API**: If you use the `--azure=<URL>` parameter, then assertions will be stored
  and retrieved via a simple web API. The server-side implementation is located in
  [here](repositories/azure/).

## Policies

A policy is a test that can be performed against one or more assertions, that evaluates to true
or false (or pass/fail, if you prefer). The purpose of a policy is to express "what is acceptable?"
based on assertions, which as mentioned above, just contain facts.

In the reference implementation, we support two types of policies:

* **Rego**: [Rego](https://www.openpolicyagent.org/docs/latest/policy-language/) is a policy
  language, part of [OpenPolicyAgent](https://www.openpolicyagent.org/). It provides a simple
  mechanism for evaluating the contents of assertions, and has a significant user base. Our support
  for Rego is currently limited; we expect to improve this support over time. You can test out
  Rego policies using the convenient [Rego Playground](https://play.openpolicyagent.org/).

* **Arbitrary Commands**: If Rego doesn't provide what you need, you can always call out to a
  custom, arbitrary command. The "Is Web Application" [sample](omega/assertion/policy/samples/)
  can help you get started.
