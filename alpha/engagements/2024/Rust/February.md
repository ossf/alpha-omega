The primary highlight of February is that all four of the scheduled threat models are now complete and available. In the beginnings of the Foundation's security initiative, we agreed to develop threat models around the crates ecosystem, the crates.io website, Rust project infrastructure and the Rust project itself. These are now all developed and will be used as guides of focus for our security work across all of these potential avenues of maliciousness.

## Threat Modeling

The four threat models being developed by the Rust Foundation are now complete:

1. **Crates ecosystem**: [Published](https://drive.google.com/file/d/1YxpJ0W5eqat2Y3ZfbdwKm_AoNhX3hIj_/).
2. **Rust Infrastructure**: [Published](https://docs.google.com/document/d/10Qlf8lk7VbpWhA0wHqJj4syYuUVr8rkGVM-k2qkb0QE/)
3. **crates.io**: [Published](https://docs.google.com/document/d/1krEL8zccid44ojS2vqxH4HRCD-bPzC7tLfcDhc5QekI/)
4. **Rust Project**: [Published](https://docs.google.com/document/d/1kpUUYekiiZRARk_EDQ7merBLmwp301yCE28MkQH-x8k/)

## Engineering

### PKI RFC

The Public Key Infrastructure (PKI) RFC has been [published](LINK TO RFC). This covers only having a base PKI and CA for the project, and the initial model for storing and accessing said keys utilizing a quorum model for ownership. This is a stepping stone towards moving to actual crate signing, mirroring, etc.

### CDN Downloads for crates.io

As described [last month](January.md), the crates.io team is working on improving the resilience of package downloads by letting cargo download them directly from the CDN servers, without having to contact the crates.io API.

The main blocker for this was the way downloads were counted. After several pull requests and deployments, crates.io is now counting downloads by parsing the CDN log files, removing the need for download requests to go through the crates.io API.

Following the work above, the crates.io team discovered another scalability issue related to updating values in the database derived from these download numbers. This was quickly addressed by optimizing the related database queries.

crates.io has been running this new download counting system for about two weeks now without any major issues. The next step of moving the download traffic away from the crates.io API is being prepared and should go into effect in March.

## Announcements

### Second Security Initiative Report

The [second security initiative report](https://foundation.rust-lang.org/news/second-security-initiative-report-details-rust-security-advancements/) has been [published](https://foundation.rust-lang.org/static/publications/security-initiative-report-february-2024.pdf), describing all the great work that has been accomplished in the year since the initiative began, along with plans for the future. 

### C++/Rust Interop Initiative

The Foundation is proud to [announce](https://foundation.rust-lang.org/news/google-contributes-1m-to-rust-foundation-to-support-c-rust-interop-initiative/) that it has been funded to support a C++/Rust Interop Initiative, to support the myriad of code where it makes sense to communicate between the two languages, but where full rewrites to Rust may be impractical. The initiative is just getting off the ground and we are about to publish a role for a full time engineer to work on the initiative.

## Rust Specification

Some progress on the Rust Specification front. The specification team has agreed upon a topic list for the specification.

```
* Front Matter
   * Introduction
   * Specification Scope
   * Terms and Definitions
* Source code and Rust syntax tree (graph?) - T-lang
    * Lexing/tokenization
    * Grammar, AST
    * Crates, modules, source files
    * Macro invocations
    * Macro expansion and conditional compilation
    * Name/Path resolution of (mod-level) items
* Static semantics - mixed T-lang/T-types
    * type checking
    * associated item resolution
    * existential (impl Trait) resolution
    * borrow checking
    * unsafe checking
    * const eval - T-opsem?
    * type inference
* Dynamic Semantics - T-opsem
    * high level expression form
    * pattern matching and binding
    * dyn traits and dynamic method dispatch
    * memory layout and value representation
    * low level (MIR-like) statement form
    * memory model (borrowing; atomics)
    * ABIs and FFI linkage
* The Core library crate - T-libs-api
    * builtin types' traits and methods
    * core::* items
    * alloc
```

This is subject to change, but the team is moving forward writing content against this outline. The team feels this outline will both allow for more efficient writing, less context switching for the reader asking questions around the how the language works and allow for use cases such as safety critical certification.