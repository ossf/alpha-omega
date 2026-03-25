# eBPF Foundation Alpha-Omega 2026 Engagement

First, thank you to Alpha-Omega for supporting the eBPF Foundation in 2026.

The purpose of this engagement is to strengthen the security of the eBPF ecosystem through two complementary workstreams:

1. an independent security assessment of core eBPF verifier and JIT execution paths; and
2. upstream engineering work to improve runtime memory-safety instrumentation for JITed eBPF programs.

The work completed to date has focused on:

- an external assessment led by STAR Labs covering the x86-64, arm64, and riscv64 eBPF JIT backends together with verifier-integration assumptions;
- validation and disclosure of verifier findings with potential impact on memory safety, pointer handling, and overall eBPF security invariants; and
- prototype implementation work to improve KASAN coverage for JITed eBPF programs, beginning with x86-64 and generic KASAN.

This directory contains progress updates for the 2026 Alpha-Omega engagement.

## 2026 Updates

- [March 2026 update](update-2026-03.md)

## Primary Contacts

- eBPF Foundation
- Linux Foundation

