"""Check lesson structure, compile every lesson script, and optionally run them.

    python tools/validate_lessons.py            # structure + syntax only
    python tools/validate_lessons.py --run      # also run learning and solutions (needs network)
    python tools/validate_lessons.py --lesson 01 --run
"""

from __future__ import annotations

import argparse
import os
import runpy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LESSONS = ROOT / "lessons"
REQUIRED = ("README.md", "{prefix}_learning.py", "{prefix}_exercises.py", "{prefix}_homework.py")


def lesson_dirs(selected: str | None) -> list[Path]:
    dirs = sorted(path for path in LESSONS.glob("lesson*") if path.is_dir())
    if selected:
        dirs = [path for path in dirs if path.name.startswith(f"lesson{selected}")]
    return dirs


def prefix_of(lesson: Path) -> str:
    return lesson.name.split("_", 1)[0]


def check_structure(lesson: Path) -> None:
    prefix = prefix_of(lesson)
    for pattern in REQUIRED:
        name = pattern.format(prefix=prefix)
        assert (lesson / name).exists(), f"{lesson.name}: missing {name}"
    assert (lesson / "fixtures").is_dir(), f"{lesson.name}: missing fixtures/"
    learning = (lesson / f"{prefix}_learning.py").read_text(encoding="utf-8")
    assert "# %%" in learning, f"{lesson.name}: learning file has no '# %%' cells"


def compile_scripts(lesson: Path) -> None:
    for script in sorted(lesson.glob("*.py")):
        compile(script.read_text(encoding="utf-8"), str(script), "exec")


def run_script(script: Path) -> None:
    previous = Path.cwd()
    os.chdir(script.parent)
    try:
        runpy.run_path(str(script), run_name="__main__")
    finally:
        os.chdir(previous)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", action="store_true", help="execute learning and solutions")
    parser.add_argument("--lesson", help="two-digit lesson number, e.g. 01")
    args = parser.parse_args()

    failed = False
    for lesson in lesson_dirs(args.lesson):
        try:
            check_structure(lesson)
            compile_scripts(lesson)
            print(f"PASS structure  {lesson.name}")
            if args.run:
                prefix = prefix_of(lesson)
                for kind in ("learning", "solutions"):
                    script = lesson / f"{prefix}_{kind}.py"
                    if not script.exists():
                        # Solutions are intentionally absent from the student repository.
                        print(f"SKIP run        {script.name} (not present)")
                        continue
                    run_script(script)
                    print(f"PASS run        {script.name}")
        except Exception as exc:  # noqa: BLE001 - report every failing lesson
            failed = True
            print(f"FAIL            {lesson.name}: {type(exc).__name__}: {exc}", file=sys.stderr)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
