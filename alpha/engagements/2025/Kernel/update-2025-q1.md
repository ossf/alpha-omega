# Linux Kernel projects update - Q1 2025


# Clang for Linux

Link to all mailing list discussions: https://lore.kernel.org/all/?q=f:nathan@kernel.org

Linux Kernel patches
 - gcc 15 fixes, needed for when clang developers change the default dialect to C23 like gcc did.
   - https://lore.kernel.org/20250121-x86-use-std-consistently-gcc-15-v1-0-8ab0acf645cb@kernel.org/
   - https://lore.kernel.org/20250122-s390-fix-std-for-gcc-15-v1-1-8b00cadee083@kernel.org/
 - warning fixes, the kernel should build warning free, so any issues that show up with newer versions of llvm need to be resolved
   - https://lore.kernel.org/20250111-spi-amd-fix-uninitialized-ret-v1-1-c66ab9f6a23d@kernel.org/
   - https://lore.kernel.org/20250116-always-inline-serialize-for-noinstr-v1-1-b7a37b2af04b@kernel.org/
   - https://lore.kernel.org/20250120-trace_events-fix-wundef-v1-1-61259cbbaa75@kernel.org/

https://nathanchance.dev/posts/january-2025-cbl-work/
https://nathanchance.dev/posts/february-2025-cbl-work/
https://nathanchance.dev/posts/march-2025-cbl-work/


# Hardening the Linux Kernel





