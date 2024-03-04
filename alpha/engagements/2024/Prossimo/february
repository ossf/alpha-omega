# Rustls
Our goal is to build a safer TLS library that can largely replace OpenSSL over time. The headline features of the new library, Rustls, are performance and memory safety.

We are making great progress. The community is also growing rapidly, with new contributors showing up regularly and largely representing new consumers of Rustls.

We accomplished a major milestone by releasing [version 0.23.0](https://github.com/rustls/rustls/pull/1817). 

  - It makes AWS's [Libcrypto](https://github.com/aws/aws-lc-rs) ("aws-lc-rs") cryptography library the default for Rustls, though users can switch between that and [*ring*](https://github.com/briansmith/ring). Soon, Microsoft's [Symcrypt](https://github.com/microsoft/SymCrypt) library will be an option, too. 
  - Libcrypto recently received FIPS support, which serves as a significant validation of its standard of security. FIPS is an important requirement for many potential government and corporate users. 

We published a [blog post](https://www.memorysafety.org/blog/rustls-with-aws-crypto-back-end-and-fips/) that summarizes this milestone and thanks Alpha-Omega for your support. 

#Rust for Linux
  
Our goal is to make Rust a supported second language for Linux kernel development, and to foster the creation of drivers and modules written in Rust.

The primary maintainer of Rust for Linux, Miguel Ojeda, has been working full time under contract with Prossimo since April of 2021.

  - The Rust project and the Rust for Linux project had their first
two "one-on-one" meetings and both projects have agreed to meet every
two weeks. This is a key step to ensure collaboration between the two
projects, in particular on topics like supporting several Rust
toolchain releases in the kernel
(https://rust-for-linux.com/rust-version-policy), the unstable
features the kernel uses
(https://rust-for-linux.com/unstable-features) and the
development/improvement of certain features in the Rust language,
library and compiler. In addition, the Rust project has created a
"rust-for-linux" stream in their Zulip. Moreover, there were other
meetings with individual Rust team members.

  - The upgrades for [Rust
1.76](https://lore.kernel.org/rust-for-linux/20240217002638.57373-1-ojeda@kernel.org/)
(current latest) and
[1.77](https://lore.kernel.org/rust-for-linux/20240217002717.57507-1-ojeda@kernel.org/)
(future release) were submitted. The former led to a discussion on how
the [jobserver was handled in
`rustc`](https://github.com/rust-lang/rust/issues/120515).

  - Rust for Linux now has ["topic
branches"](https://rust-for-linux.com/branches#topic-branches). This
is the result of increasing interest from several parties in an
arrangement that would allow collaboration between different entities
on particular subsystems that cannot be upstreamed into the kernel yet
for different reasons. The first ones are `rust-pci` and `rust-net`,
as well as a DRM one that may live in their own repository.

  - GCC Rust now has a [page in the Rust for Linux
website](https://rust-for-linux.com/gccrs), maintained by the GCC Rust
maintainers.
