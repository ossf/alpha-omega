# Omega Assertion Framework

The Omega Assertion Framework (OAF) is a series of tools for generating assertions reflecting facts
about a subject, and for consuming those assertions through policies.

OAF was designed to allow organization

## Assertions

Assertions are "facts" about a subject, such as, "The weather in Washington was rainy yesterday."
Assertions can be signed, so that a consumer can be sure that someone they trust created the
assertion.

Assertions are formatted as JSON, with a few key fields:

* predicateType
* predicate

