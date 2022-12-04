## Compression Fuzzing

This directory contains scripts and other information related to fuzzing
compression tools, like gzip and lz4.

It currently uses [Radamsa](https://gitlab.com/akihe/radamsa) to mutate
a generated compressed file and looks for crashes during decompression.

