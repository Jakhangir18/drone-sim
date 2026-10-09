# Robot arm simulator

Simulation of a robot arm in MuJoCo, to be driven later by a human input device. Aslo i just want to metio that we need also work on jostics (i mean animation where you can yse ur jostion for VR and then there would nice animation how robot make the same movemts)



(a "bracelet", exact device not yet known maybe ). Course project for
Prof. Raffaele De Amicis, Oregon State.

This repository started as a drone simulator. That work stopped in October 2026
and lives in `archive/drone/` for reference. Nothing in there is used.

## Setup

Both scripts create `.venv` with Python 3.12 and install `requirements.txt`
(`mujoco==3.11.0` is the main dependency). Run once per machine after
`git clone`. VS Code finds `.venv` on its own on both systems.

**Windows (desktop):**

```powershell
.\setup.ps1
.\.venv\Scripts\python.exe some_script.py
```

**macOS (laptop):** needs Python 3.12 first, e.g. `brew install python@3.12`.

```bash
./setup.sh
.venv/bin/python some_script.py      # headless scripts
.venv/bin/mjpython some_viewer.py    # anything that opens the MuJoCo viewer
```

On macOS the viewer must run under `mjpython`, not `python`. The OS requires the
GUI loop to own the main thread; plain `python` raises a RuntimeError from
`launch_passive`.

## Running



so here what do you need to run it 

cd ~/drone-sim

.venv/bin/python -m mujoco.viewer --mjcf="$PWD/assets/shadow_hand/scene_right.xml"


Nothing runs yet. The arm model is chosen in lesson 1 (see `LESSONS.md`) and
scripts appear as the lessons are completed.

## Documents

| File | What it is |
|---|---|
| `LESSONS.md` | The curriculum: one concept per lesson, task, numeric check |
| `LOG.md` | Learning log: what was done, what was learned, what is unclear |
| `CLAUDE.md` | Rules for Claude Code here: teach, do not just give answers |
| `TECHNOLOGY_RESEARCH.md` | Why MuJoCo over Isaac Lab, and the device-adapter architecture |
| `.claude/skills/robot-arm/` | Project context for Claude: invariants, decisions, stop-and-ask points |
| `archive/drone/` | The previous drone project, kept for history |

## Working rules

- Pull at the start of a session, push at the end. Every lesson ends in a pushed commit.
- Never judge correctness by looking at the viewer. Every script asserts a number
  computed independently.
- Never commit `.venv/`.
