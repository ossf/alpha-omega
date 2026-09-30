# About Trifecta Tech Foundation

Trifecta Tech Foundation is a non-profit recognized by the Netherlands Tax Authority as a Public
Benefit Organisation (ANBI). Our mission is to make critical infrastructure software safer by decreasing attack surface: by building software that is robust and inherently safer.

Our projects are organized in three initiatives:

- Time synchronization
- Privilege boundary
- Data compression, 

Projects such as zlib-rs (part of Firefox), sudo-rs (default sudo on Ubuntu), and ntpd-rs that runs in the Let's Encrypt infrastructure, impact the digital security of hunderds of millions of people.

## Alpha Engagement: memory-safe Zstandard encoder

This project aims to show how you can effectively create memory-safe drop-in replacements using
translation tools and AI-assisted cleanup.

Zstandard is a modern successor to zlib, providing better compression faster. Our Zstandard in
Rust project, libzstd-rs-sys, is a drop-in compatible zstd implementation written in Rust. The
implementation will be correct (it has equivalent behavior to the reference implementation),
performant, and usable as both a static and a dynamic library, just like the reference
implementation.

libzstd-rs-sys is in development, and the decoder is completed. As part of this engangement we will deliver the encoder, completing the full Zstandard functionality.

## Technical approach

Building on our previous experience in porting and translating data compression software, this
project aims to show how you can effectively create memory-safe drop-in replacements using
translation tools and AI-assisted cleanup to port C/C++ software to Rust.

In previous translation efforts, we opted for a manual approach to improve the automatically translated code. The initial output of translation is low quality code, and the effort to improve it ("cleanup") is substantial. Much of the cleanup work is mechanical, uninteresting for maintainers, and suitable for LLMs.

The translation-plus-LLM-aided-cleanup approach comes with trade offs. Automating the porting work is a short-term win, but it causes long-term maintenance issues. Working with the code is important for maintainers to build knowledge of the codebase. As part of the project we will address maintainability by conducting knowledge building activities outside the building process.




