# Robot arm simulator

Simulation of a robot arm in MuJoCo, to be driven later by a human input device
(a "bracelet", exact device not yet known). Course project for
Prof. Raffaele De Amicis, Oregon State.

This repository started as a drone simulator. That work stopped in October 2026
and lives in `archive/drone/` for reference. Nothing in there is used.

## Setup (Windows)

```powershell
.\setup.ps1
```

Creates `.venv` with Python 3.12 and installs `requirements.txt`
(`mujoco==3.11.0` is the main dependency). Works the same on any Windows machine
after `git clone`, so the desktop and the laptop stay identical.

VS Code picks up `.venv\Scripts\python.exe` automatically via
`.vscode/settings.json`.

## Running

Nothing runs yet. The arm model is chosen in lesson 1 (see `LESSONS.md`) and
scripts appear as the lessons are completed.

## Documents

| File | What it is |
|---|---|
| `LESSONS.md` | The curriculum: one concept per lesson, task, numeric check |
| `LOG.md` | Learning log: what was done, what was learned, what is unclear |
| `TECHNOLOGY_RESEARCH.md` | Why MuJoCo over Isaac Lab, and the device-adapter architecture |
| `.claude/skills/robot-arm/` | Project context for Claude: invariants, decisions, stop-and-ask points |
| `archive/drone/` | The previous drone project, kept for history |

## Working rules

- Pull at the start of a session, push at the end. Every lesson ends in a pushed commit.
- Never judge correctness by looking at the viewer. Every script asserts a number
  computed independently.
- Never commit `.venv/`.
