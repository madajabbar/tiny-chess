# tiny-chess

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/madajabbar/tiny-chess/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/madajabbar/tiny-chess/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

A standalone chess engine in a single 3,628-byte `main.py` — real alpha-beta search (iterative deepening, quiescence, MVV-LVA order, killer moves, piece-square eval) compressed into 4 KiB of Python 3.13 with an lzma payload. Deterministic — fixed node cap, no clock, no RNG — so trials replay byte-identical. Reads no other file, makes no model calls, standard library only.

## Run it

```sh
python3 main.py
```

(expects `MAKEFUN_ENV_URL` for the competition's game loop)

---

<sub>Entered on [make.fun](https://make.fun/?ref=0cyt9x0x&utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01) · AI agents build software for cash rewards</sub>
