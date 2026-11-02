# **eBPF Foundation Alpha-Omega Engagement**

## **Project Update — October 2026**

This update covers engineering progress through October 2026 for the eBPF Foundation's engagement under the OpenSSF Alpha-Omega program. Work during this period achieved a major milestone with the upstream acceptance and merge of Kernel Address Sanitizer (KASAN) support for x86\_64 JITed eBPF programs into the bpf-next kernel tree. Additional efforts focused on refining verifier fixup tracking, expanding selftest validation matrices, landing CI infrastructure improvements to handle expected sanitizer reports, and preparing community presentations for the Linux Plumbers Conference (LPC).

### **RFC Review and Community Engagement**

* **Upstream Acceptance into bpf-next:** Following multiple review iterations throughout August and early September, the patch series implementing KASAN support for the x86\_64 eBPF JIT compiler was merged into the upstream bpf-next tree on September 7, 2026\.  
* **Revision v9 Progression:** Prior to merge, revision v9 was submitted to address reviewer feedback on register sanitization, memory bitfield representations, and instruction-level isolation. The revision resolved corner cases surrounding function call argument handling on the stack (BPF\_REG\_PARAMS) introduced in recent toolchain versions.  
* **Conference and Community Outreach:** Technical slides and presentation materials were prepared for the Linux Plumbers Conference (LPC) in early October 2026\. Alongside conference preparations, drafting commenced on a comprehensive technical article detailing runtime memory safety mechanisms and verification boundaries within the eBPF ecosystem.

### **Expanded Instruction Coverage**

Kernel Address Sanitizer (KASAN) is a dynamic memory error detector designed to intercept and report out-of-bounds memory accesses and use-after-free conditions in the Linux kernel. Historically, JITed eBPF programs operated without dynamic sanitization, relying exclusively on static verification at program load time. The accepted implementation instruments memory dereferences directly within the JIT compiler, providing runtime protection against memory safety violations that bypass verification or originate in kernel-managed structures.

* **Memory Operation Coverage:** Instrumentation was established across standard load and store operations (BPF\_LDX, BPF\_STX, and BPF\_ST) by emitting calls to \_\_asan\_load\* and \_\_asan\_store\* runtime functions prior to memory access. Immediate store operations (BPF\_ST) were refactored to align cleanly with native instruction generation on x86\_64.  
* **Atomic Instruction Instrumentation:** Support was implemented for atomic memory operations (BPF\_ATOMIC), encompassing atomic operations with and without fetch semantics (BPF\_FETCH), such as atomic add, bitwise logic, and compare-and-swap loops. Memory operands are checked prior to executing locked instructions, preventing corrupted memory manipulation during concurrent execution.  
* **Fault-Tolerant Instruction Handling:** Explicit exemptions were implemented for speculative and probe-based operations, including BPF\_PROBE\_MEM, BPF\_PROBE\_ATOMIC, and BPF\_NOSPEC. Because these instructions deliberately handle non-canonical or potentially unmapped addresses with kernel exception table fixups, instrumenting them would cause unrecoverable page faults in KASAN shadow memory translation.

### **Testing and Validation**

* **Verifier Fixup and Stack Tracking:** To avoid redundant instrumentation on known-safe program stack slots, instruction metadata was integrated into env-\>insn\_aux\_data to mark stack-targeting instructions. When the verifier rewrites instructions—such as during constant blinding (bpf\_jit\_harden), 32-bit zero/sign extensions, or helper inlining—the tracking logic was adapted to maintain correct instruction offsets and prevent unintended instrumentation skips.  
* **Toolchain Compatibility (Clang 23):** Validation was carried out against Clang 23.1.0 builds to test compatibility with the new stacked arguments feature (\_\_BPF\_FEATURE\_STACK\_ARGUMENT), ensuring programs receiving more than five arguments compute stack offsets accurately when instrumentation is applied.  
* **Expanded Selftest Suite:** A dedicated test runner was developed within test\_progs exercising invalid reads and writes across 1-, 2-, 4-, and 8-byte access widths, atomic operations, and deliberate use-after-free and out-of-bounds scenarios. Tests leverage synthetic shadow-memory poisoning helpers in bpf\_testmod to reliably test sanitizer behavior without inducing kernel panics.  
* **CI Log Harvesting and Allowlisting:** Programmatic validation was added using klogctl to scrape kernel rings and confirm report generation during test execution. To support automated testing without tripping test harness failures, Pull Request \#520 was merged into the upstream vmtest repository to introduce SPLAT\_ALLOWLIST support, enabling expected KASAN splats to pass CI cleanly.

### **Additional Engineering Progress**

* **Network Selftest Stability:** Resolved transient race conditions in the network tunneling test suites (tc\_tunnel and tc\_edt), where non-blocking socket connection establishment occasionally failed under high host CPU load with EINPROGRESS. Connection helpers were adjusted to ensure reliable polling across virtualized environments.  
* **Selftest Suite Consolidation:** Continued evaluation and migration of legacy standalone test scripts toward the unified test\_progs harness to increase automated regression coverage in standard kernel CI.

## **Current Focus**

* Monitoring upstream bpf-next CI matrices following the KASAN merge to track runtime stability across diverse configurations.  
* Presenting the eBPF JIT KASAN architecture, verifier interaction model, and implementation results at the Linux Plumbers Conference (LPC).  
* Completing and publishing the technical overview covering runtime memory safety for the broader eBPF community.  
* Investigating architecture requirements, ABI constraints, and calling conventions for porting KASAN instrumentation to the ARM64 (aarch64) JIT compiler.  
* Continuing the migration and cleanup of remaining standalone selftests into the unified test runner.

## **Acknowledgements**

The eBPF Foundation thanks Alpha-Omega for its continued support of this work. The engagement is helping advance practical security improvements for the Linux kernel and the broader eBPF ecosystem through both upstream engineering and community collaboration.
