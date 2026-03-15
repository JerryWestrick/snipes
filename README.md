# Snipes

[![PyPI](https://img.shields.io/pypi/v/snipes-game)](https://pypi.org/project/snipes-game/)
[![Python](https://img.shields.io/pypi/pyversions/snipes-game)](https://pypi.org/project/snipes-game/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A Python/Pygame recreation of the classic 1983 Novell NetWare game.

The original Snipes was one of the first network games for personal computers, created by Drew Major, Dale Neibaur, and Kyle Powell to test and debug Novell's networking software. This version brings the gameplay to modern systems using Pygame.

## Gameplay

Navigate a randomly generated maze, destroy enemy hives and the snipes they spawn. Clear all hives and snipes to advance to the next level.

- **9 levels** with increasingly larger mazes, more hives, faster and more numerous enemies
- **8-direction shooting** — combine two keys for diagonal shots
- **Diagonal shots ricochet** off walls — bank shots around corners
- Score and lives carry across levels

## Controls

| Keys       | Action                      |
|------------|-----------------------------|
| Arrow keys | Move (combine for diagonal) |
| W A S D    | Shoot (combine for diagonal)|
| P          | Pause                       |
| ESC        | Quit                        |

## Install

```bash
pipx install snipes-game
```

Or with pip:

```bash
pip install snipes-game
```

Or from source:

```bash
git clone https://github.com/JerryWestrick/snipes.git
cd snipes
pip install .
```

## Run

```bash
snipe
```

Or:

```bash
python -m snipe
```

## About the Original

Snipes (1983) was written for Novell NetWare and is considered one of the first network games for personal computers. It was originally created to test Novell's networking code. Players navigated a text-mode maze, shooting at enemies and destroying their generators. This recreation preserves the core gameplay while using modern pixel-based rendering with Pygame.

## License

MIT
