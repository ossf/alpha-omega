We [announced](https://www.memorysafety.org/blog/rustls-and-rust-for-linux-funding-openssf/) the OpenSSF Alpha-Omega grant alongside the Open Source Summit Europe's OpenSSF Day. 

# Rustls

Our goal is to build a safer TLS library that can largely replace OpenSSL over time. The headline features of the new library, Rustls, are performance and memory safety.

We are making great progress. The community is also growing rapidly, with new contributors showing up regularly and largely representing new consumers of Rustls.

The pluggable cryptography implementation started to land in August and work is under way to add support for [aws-lc-rs](https://github.com/rustls/rustls/tree/jbp-try-aws-lc-rs). This has been a huge amount of work. We expect the pluggable cryptography implementation and aws-lc-rs integration to be completed in October. We are waiting on guidance from the aws-lc-rs team regarding finalizing FIPS support.

Adolfo Ochogavia is making great progress on [benchmarking](https://github.com/rustls/rustls/issues/1487) and his benchmarking tools are already being used by Rustls developers to improve performance.

Ferrous Systems has largely completed an RFC for caller managed buffers, asynchronous APIs, and no-std support. Implementation has started.

Previously, work under Prossimo contracts has led to:

A major new release announced on March 30th, adding support for some of the most heavily requested features, including IP address support, C.4 session caching, and a number of API improvements. 
A release on July 7 adding CRL support, particularly important for client certificate support.
Numerous other fixes and improvements along the way.



# Linux Kernel
Our goal is to make Rust a supported second language for Linux kernel development, and to foster the creation of drivers and modules written in Rust.

The primary maintainer of Rust for Linux, Miguel Ojeda, has been working full time under contract with Prossimo since April of 2021.

 - Linux v6.6-rc1 was released on September 11th, which includes the
[Rust v6.6 PR](https://lore.kernel.org/rust-for-linux/20230824214024.608618-1-ojeda@kernel.org/)
as well as the [KUnit
one](https://lore.kernel.org/all/f786a4f9-93f3-716b-3f7f-a3f7b4c889f4@linuxfoundation.org/).
- The workqueue abstractions [have been
applied](https://lore.kernel.org/rust-for-linux/ZRHkRpZJemtn67rf@slm.duckdns.org/)
for v6.7.
- Both [Cisco](https://rust-for-linux.com/industry-and-academia-support#Cisco)
and [Collabora](https://rust-for-linux.com/industry-and-academia-support#Collabora)
released statements of support, joining the list of companies publicly
supporting the Rust for Linux effort.
- Kangrejos 2023: the [workshop](https://kangrejos.com) took place
this month and was a success. There were 27 attendees, including the Rust
for Linux core team and other Linux kernel maintainers. Engineers from
key companies like Canonical, Cisco, Collabora, Ferrous Systems,
Google, LWN, Meta, Microsoft, Oracle, Samsung and Red Hat were
present.
- LPC 2023: the [Rust for Linux
talk](https://lpc.events/event/17/contributions/1501/) has been
accepted for the Refereed track. In addition, the talks and schedule
of the [Rust Microconference](https://lpc.events/event/17/sessions/170/)
have been published.
- Linux Kernel Maintainer Summit: a [Rust
topic](https://lore.kernel.org/ksummit/CANiq72=99VFE=Ve5MNM9ZuSe9M-JSH1evk6pABNSEnNjK7aXYA@mail.gmail.com/)
has been proposed.
