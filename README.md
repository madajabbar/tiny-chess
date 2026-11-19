# tiny-chess-01 — a tiny chess engine

A standalone chess engine entered in the make.fun **tiny-chess-01** bounty. Single file, 3,628 bytes, Python 3.13 standard library only.

## The engine

`main.py` is a real alpha-beta chess search compressed into 4 KiB:

- **Board**: 0x88 mailbox, legal move generation.
- **Search**: negamax alpha-beta with iterative deepening, capped at 40,000 nodes/move (deterministic — no clock, no RNG, so trials replay byte-identical).
- **Quiescence**: captures, en-passant, promotions, full evasions when in check.
- **Ordering**: MVV-LVA captures first, one killer move per ply, queen-promotion priority.
- **Eval**: material (P=100 N=320 B=330 R=500 Q=900) + PeSTO-simplified piece-square tables, side-relative.
- **I/O**: speaks the competition's game loop — `POST /game`, `POST /move` with UCI, long-polls until `done`.

## Build

`main.py` is an `lzma`-compressed payload (preset 9/EXTREME, base85) unpacked at import time. The unpacker + payload together are the 3,628 committed bytes. `main.py` reads no other file, makes no model calls, and is fully deterministic.

## Verify

```sh
python3 -c "import ast; ast.parse(open('main.py').read())"   # parses
python3 main.py                                               # expects MAKEFUN_ENV_URL
wc -c main.py                                                 # 3628 ≤ 4096
```

Self-tested: perft 20/20 (startpos d1–d4, kiwipete, positions 3–6), determinism + legality on 40 random positions, and a mock-server run winning 4 games by checkmate at ~2s/move.

## License

MIT (see LICENSE).
