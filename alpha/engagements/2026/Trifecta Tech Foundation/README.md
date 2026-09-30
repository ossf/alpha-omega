# Alpha Engagement: Trifecta Tech Foundation

The purpose of this engagement is to complete [libzstd-rs](https://github.com/trifectatechfoundation/libzstd-rs-sys), a memory-safe, drop-in
compatible implementation of Zstandard (zstd) written in Rust. Zstandard is a modern alternative to zlib, providing better data compression, faster. It is widely deployed and handles untrusted input, which makes a memory-safe implementation valuable for critical infrastructure.

The libzstd-rs *decoder* is already complete. This engagement delivers the *encoder*, so that
libzstd-rs is a complete alternative to the C reference implementation, as a static or dynamic library, with equivalent behavior and on-par performance.

The implementation method uses automated translation from C to Rust as a starting point. We will compare translation approaches, and address a challenge that comes with translation projects: long-term maintainability.

## Deliverables

- A complete, audited, memory-safe drop-in compatible Zstandard encoder in libzstd-rs
- A comparison of porting methods: translation tooling (`c2rust`) followed by manual cleanup
  (as we used for the decoder) versus translation followed by LLM-assisted cleanup
- A report on the lessons learned about long-term maintainability of translated projects

## Timeline

The timeline for the project, including release and report is 9 months.
Starting in September 2026, we expect to finish the project in May 2027.

## Monthly updates

- [September 2026](2026-09.md)

## Primary Contacts

- Erik Jonkers - Chair of the board
- Folkert de Vries - Lead maintainer

## About the approach and maintainability

Building on our previous experience in porting and translating data compression software, this
project will use the translation tool `c2rust` and LLM-assisted improvements to port the C software to Rust.

In previous efforts, we opted for a manual approach to improve the automatically translated code. The process included a significant effort to improve (clean up) the initial translation to safe, high-quality code. Much of that cleanup work proved to be mechanical, high-effort and uninteresting for maintainers, but suitable for LLMs. Based on small-scale experimentation, we've observed that LLMs can easily pattern-match on the many small commits (from the decoder implementation) in this codebase and replicate the changes.

Although LLMs can further improve efficiency, any translation approach comes with a trade-off: automating the porting work can be a short-term win, but it causes long-term maintenance issues. Building software builds expertise. Porting software, in an automated way, does not, or at least not to the same extent.

We will therefore pair the translation effort with activities that build maintainer knowledge of the codebase, with the goal of providing guidelines for workflows that remove grunt work without sacrificing long-term maintainability.

## About Trifecta Tech Foundation

[Trifecta Tech Foundation](https://trifectatech.org) is a non-profit recognized by the Netherlands Tax Authority as a Public Benefit Organisation (ANBI). Our mission is to make critical infrastructure software safer by decreasing attack surface: by building software that is robust and inherently safer.

Our projects are organized in three initiatives:

- Time synchronization
- Privilege boundary
- Data compression 

Projects such as zlib-rs (part of Firefox), sudo-rs (default sudo on Ubuntu), and ntpd-rs that runs in the Let's Encrypt infrastructure, are strong examples of how our work impacts the digital security of millions of people.