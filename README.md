# c64

A Commodore 64 running on the PlayStation, built on [nugget](https://github.com/pcsx-redux/nugget) and PSYQo.

- `m6502bench/`: a 6502 interpreter and a 6502-to-MIPS recompiler, benchmarked on Klaus Dormann's functional test.
- `c64/`: the machine (NTSC VIC-II text modes, both CIAs, banking) on top of that core. It boots to READY.

ROMs are the MEGA65 Open ROMs (LGPL-3), and the Dormann test binary is GPL-3. Both are fetched at build time and never
committed here.

```
git clone --recursive https://github.com/ps1dev/c64
make -C c64/c64
```

`EXTRA=-DC64_JIT_ONLY` or `EXTRA=-DC64_INTERP` picks one core. The default build alternates the two in 300-frame windows
after READY. and prints timings over the TTY. make does not track `EXTRA`, so remove `*.o *.dep` between variants.
