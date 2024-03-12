# Rustls
Our goal is to build a safer TLS library that can largely replace OpenSSL over time. The headline features of the new library, Rustls, are performance and memory safety.

We are making great progress. The community is also growing rapidly, with new contributors showing up regularly and largely representing new consumers of Rustls.

The Rustls developers spent January primarily building towards the first release with the [aws-lc-rs](https://github.com/aws/aws-lc-rs) cryptographic back-end as the default, which will include FIPS support. This is one of the most important remaining features that need to be implemented before significantly more widespread adoption is possible. The release with the work can be expected in early February.

The team also [merged](https://github.com/rustls/rustls/pull/1597) [no-alloc API support](https://github.com/rustls/rustls/pull/1399) in January, which is important for high performance consumers, and have made a number of other miscellaneous improvements.

The team completed, merged, and shipped an excellent benchmarking system, both to catch performance regressions on a per-commit basis and to compare Rustls to OpenSSL. We published a summary of the work and outcomes in this [blog post](https://www.memorysafety.org/blog/rustls-performance/).

# Rust for Linux
  
Our goal is to make Rust a supported second language for Linux kernel development, and to foster the creation of drivers and modules written in Rust.

The primary maintainer of Rust for Linux, Miguel Ojeda, has been working full time under contract with Prossimo since April of 2021. In the past month, he continued work on the new build system for the Rust side of the Linux kernel, among a bevy of other project management, momentum building, and technical contributions. 

A few highlights from the last month: 

  - The usual Rust PR was [merged for
v6.8](https://lore.kernel.org/rust-for-linux/20240108012055.519813-1-ojeda@kernel.org/).

  - The first Linux driver written in Rust (a PHY "reference" driver)
was [merged for
v6.8](https://lore.kernel.org/lkml/20240109162323.427562-1-pabeni@redhat.com/),
together with the required PHY abstractions.

  - Initial Rust support for the LoongArch architecture [landed for
v6.8](https://lore.kernel.org/lkml/20240119110700.335741-1-chenhuacai@loongson.cn/).
arm64 should also be landing soon and RISC-V is also getting ready to
land it.

  - An [initial kernel CI for `rustc_codegen_gcc`
builds](https://github.com/Rust-for-Linux/ci-rustc_codegen_gcc) has
been setup, which does not require any kernel patches and uses the
backend almost as-is from the Rust repository. It will be maintained
by the `rustc_codegen_gcc` project itself. This represents the start
of regular testing of GCC kernel builds with Rust enabled. As soon as
the CI is deemed stable enough, the plan is to incorporate such builds
into the kernel CI, documentation, etc.
