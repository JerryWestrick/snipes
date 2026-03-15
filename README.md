# Snipes

A Python/Pygame recreation of the classic 1983 Novell NetWare game.

The original Snipes was one of the first network games for personal computers, created by Drew Major, Dale Neibaur, and Kyle Powell to test and debug Novell's networking software. This version brings the gameplay to modern systems using Pygame.

## Gameplay

Navigate a randomly generated maze, destroy enemy hives and the snipes they spawn. Clear all hives and snipes to advance to the next level.

- **9 levels** with increasingly larger mazes, more hives, faster and more numerous enemies
- **8-direction shooting** — combine two keys for diagonal shots
- **Diagonal shots ricochet** off walls — bank shots around corners
- Score and lives carry across levels

## Controls

| Keys | Action |
|------|--------|
| Arrow keys | Move |
| W A S D | Shoot (combine for diagonals) |
| P | Pause |
| ESC | Quit |

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install pygame-ce
```

## Run

```bash
python main.py
```

## Requirements

- Python 3.10+
- pygame-ce
