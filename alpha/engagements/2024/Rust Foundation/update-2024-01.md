As we pick the security initiative work up for 2024, the highlight of January is that we are now able to replay crate publishing from the past. This provides a retrospective on what new [Typomania](https://github.com/rustfoundation/typomania) and Sandpit checks would have found, and thus find in the future.

## Threat Modeling

Here is the progress on the four threat models being developed by the Rust Foundation:

1. **Crates ecosystem**: [Published](https://drive.google.com/file/d/1YxpJ0W5eqat2Y3ZfbdwKm_AoNhX3hIj_/).
2. **Rust Infrastructure**: [Published](https://docs.google.com/document/d/10Qlf8lk7VbpWhA0wHqJj4syYuUVr8rkGVM-k2qkb0QE/)
3. **crates.io**: Nearly complete. Plan to publish in early February.
4. **Rust Project**: Nearly complete. Plan to publish in early February.

## Engineering

### Crate Publishing Replay

We are now able to replay crate publishing from the past, allowing us to use historical data to evaluate the efficacy of specific Typomania and Sandpit checks. We intend to use this to establish a scoring system on potential maliciousness, which — if a crate falls above a given threshold — can feed into deciding whether to quarantine the crate and potentially that user pending further review.

We will continue to improve tooling for retrospective crate analysis.

### Sandpit deploy to production

Sandpit, our tool that scans available crates to try to detect malicious crates based on available heuristics, has been deployed to production on Google Cloud Platform (GCP) and is running at a regular cadence.

### CDN Downloads for crates.io

crates.io is currently counting downloads in the application's backend. Given the high volume of requests to the /download endpoint, this is starting to cause performance issues. From the perspective of the crates team, it would be preferable to avoid serving download requests through the application and instead serve them directly from the CDN. But this will require a new solution for counting crate downloads.

The proposed approach is to count downloads based on the request logs. This would provide a scalable mechanism that counts downloads in batches, reducing the load on the backend and database. Request logs are currently uploaded to S3 from both CloudFront and Fastly. The format of the logs differs greatly, but both contain the requested URL which can be used to determine the crate name and version.

Ultimately, this will allow cargo to download crates directly from static.crates.io, which means if crates.io has issues the downloads will keep working and the whole system will scale a lot better than before.

The first [PR](https://github.com/rust-lang/crates.io/pull/8010) for crates.io towards this goal is now available.

## Community

### Typosquatting Blog Post

Adam is nearly finished with a two-part blog post on typosquatting and Typomania, going into technical details as they relate to crates.io, etc. One blog post will be posted on the [Foundation website](https://rustfoundation.org). The other blog post will posted on the [Rust Insider website](https://blog.rust-lang.org/inside-rust/).

Adam is also documenting the process to be followed when handling malicious crates, which allows other crates.io team members to handle malicious crates in a way that ensures we preserve the malware and all the metadata needed to facilitate future analysis and reporting to upstream(s) and/or law enforcement, as appropriate.

Adam and Walter have submitted talks for consideration at [Open Source Summit North America](https://events.linuxfoundation.org/open-source-summit-north-america/program/cfp/#overview) and the accompanying [SOSS Community Day](https://openssf.org/blog/2024/01/11/submit-to-speak-at-soss-community-day-north-america-2024/).

Walter and JD have talks scheduled at [Rust Nation UK](https://www.rustnationuk.com/schedule) in March.

Rust specification work has officially gotten off the ground with [sample chapters](https://rust-lang.zulipchat.com/#narrow/stream/399173-t-spec/topic/Feedback.20on.20spec.20samples) being written in order to guide specification format, flow, tools needed to generate a readable specification, and more.