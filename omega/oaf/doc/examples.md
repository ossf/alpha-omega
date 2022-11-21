# OAF Example Usage


## Generating Assertions

### Security Advisories

This assertion consults the [deps.dev](https://deps.dev) website for details
on CVEs or GitHub security advisories that affect the subject. If any are
found, the aggregate results are stored in the predicate and the raw result
from the website are stored as evidence.

```json
//python oaf.py generate --assertion=SecurityAdvisory
//                       --subject=pkg:pypi/django@4.0.
{
  "_type": "https://in-toto.io/Statement/v0.1",
  "predicate": {
    "content": {
      "security_advisories": {
        "critical": 1,
        "high": 2,
        "medium": 1,
        "unknown": 10
      }
    },
    "evidence": {
      "_type": "https://github.com/ossf/alpha-omega/types/evidence/url/v0.1",
      "content": "(removed)"
    }
  }
}
```

### Programming Languages

This assertion identifies which programming languages and file extensions
are in use within a subject. It uses the output from
[Application Inspector](https://github.com/Microsoft/ApplicationInspector),
for the actual analysis. It therefore requires the `input-file` parameter,
pointing to such output.




## Digital Signatures

To add a digital signature, add a `--signer=<path to private key>` to the generate action.
To verify, do the same thing for the consume action.

Only PEM files (private-key.pem) are currently supported.

You can generate a simple key pair using OpenSSL:

```
openssl ecparam -name prime256v1 -genkey -noout -out private-key.pem
openssl ec -in private-key.pem -pubout -out public-key.pem
```

**Important*: The digital signature scheme will definitely change before we stabilize.

## Expiration

Assertions can be generated with a "shelf-life", described in an `expiration` field, which you
can set via the command line.

```json
// python oaf.py generate --assertion=SecurityAdvisory --subject=pkg:npm/left-pad@1.3.0 --expiration=2023-12-31
{
  "_type": "https://in-toto.io/Statement/v0.1",
  "predicate": {
    "operational": {
      "expiration": "2023-12-31T00:00:00.000000Z"
    }
  }
}
```