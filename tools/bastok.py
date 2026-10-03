#!/usr/bin/env python3
# Tokenizes a Commodore BASIC V2 listing into a .prg loading at $0801.
# usage: bastok.py in.bas out.prg
import sys

KEYWORDS = [
    "END", "FOR", "NEXT", "DATA", "INPUT#", "INPUT", "DIM", "READ", "LET", "GOTO", "RUN", "IF", "RESTORE",
    "GOSUB", "RETURN", "REM", "STOP", "ON", "WAIT", "LOAD", "SAVE", "VERIFY", "DEF", "POKE", "PRINT#",
    "PRINT", "CONT", "LIST", "CLR", "CMD", "SYS", "OPEN", "CLOSE", "GET", "NEW", "TAB(", "TO", "FN",
    "SPC(", "THEN", "NOT", "STEP", "+", "-", "*", "/", "^", "AND", "OR", ">", "=", "<", "SGN", "INT",
    "ABS", "USR", "FRE", "POS", "SQR", "RND", "LOG", "EXP", "COS", "SIN", "TAN", "ATN", "PEEK", "LEN",
    "STR$", "VAL", "ASC", "CHR$", "LEFT$", "RIGHT$", "MID$", "GO",
]
# Longest match first, the way the ROM's cruncher effectively behaves for these.
ORDER = sorted(range(len(KEYWORDS)), key=lambda i: -len(KEYWORDS[i]))


def crunch(text):
    out = bytearray()
    i = 0
    quoted = False
    rem = False
    while i < len(text):
        ch = text[i]
        if quoted or rem:
            out.append(ord(ch))
            if ch == '"':
                quoted = False
            i += 1
            continue
        if ch == '"':
            quoted = True
            out.append(ord(ch))
            i += 1
            continue
        for k in ORDER:
            kw = KEYWORDS[k]
            if text.startswith(kw, i):
                out.append(0x80 + k)
                i += len(kw)
                if kw == "REM":
                    rem = True
                break
        else:
            out.append(ord(ch))
            i += 1
    return out


def main():
    src, dst = sys.argv[1], sys.argv[2]
    addr = 0x0801
    body = bytearray()
    for line in open(src):
        line = line.strip()
        if not line:
            continue
        num, rest = line.split(" ", 1)
        tok = crunch(rest)
        nxt = addr + len(body) + 4 + len(tok) + 1
        body += bytes([nxt & 0xFF, nxt >> 8, int(num) & 0xFF, int(num) >> 8]) + tok + b"\0"
    body += b"\0\0"
    open(dst, "wb").write(bytes([addr & 0xFF, addr >> 8]) + body)


main()
