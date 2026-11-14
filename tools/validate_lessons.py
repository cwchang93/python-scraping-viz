"""Check lesson structure and notebook cell syntax, and optionally execute notebooks.

    python tools/validate_lessons.py            # structure + syntax only
    python tools/validate_lessons.py --run      # also run learning and solutions (needs network)
    python tools/validate_lessons.py --lesson 01 --run

Notebook cells are executed in order with HEADLESS=1 when --run is requested.
"""

from __future__ import annotations

import argparse
import os
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LESSONS = ROOT / "lessons"
REQUIRED = ("README.md", "{prefix}_learning.ipynb", "{prefix}_exercises.ipynb", "{prefix}_homework.ipynb")


def lesson_dirs(selected: str | None) -> list[Path]:
    dirs = sorted(path for path in LESSONS.glob("lesson*") if path.is_dir() and not path.name.startswith("lesson00_"))
    if selected:
        dirs = [path for path in dirs if path.name.startswith(f"lesson{selected}")]
    return dirs


def prefix_of(lesson: Path) -> str:
    return lesson.name.split("_", 1)[0]


def check_structure(lesson: Path) -> None:
    prefix = prefix_of(lesson)
    is_warmup = lesson.name.endswith("_python_warmup")
    required = ("README.md", "{prefix}_learning.ipynb") if is_warmup else REQUIRED
    for pattern in required:
        name = pattern.format(prefix=prefix)
        assert (lesson / name).exists(), f"{lesson.name}: missing {name}"
    if not is_warmup:
        assert (lesson / "fixtures").is_dir(), f"{lesson.name}: missing fixtures/"
    notebook = json.loads((lesson / f"{prefix}_learning.ipynb").read_text(encoding="utf-8"))
    assert notebook.get("nbformat") == 4 and notebook.get("cells"), f"{lesson.name}: invalid notebook"


def compile_scripts(lesson: Path) -> None:
    for notebook in sorted(lesson.glob("*.ipynb")):
        data = json.loads(notebook.read_text(encoding="utf-8"))
        for index, cell in enumerate(data["cells"], 1):
            if cell["cell_type"] == "code":
                compile("".join(cell["source"]), f"{notebook}:cell {index}", "exec")


def run_script(script: Path) -> None:
    previous = Path.cwd()
    previous_argv = sys.argv
    os.chdir(script.parent)
    os.environ["HEADLESS"] = "1"
    sys.argv = [str(script)]  # scripts read sys.argv themselves (lesson09_learning.py takes unit numbers)
    try:
        notebook = json.loads(script.read_text(encoding="utf-8"))
        namespace = {"__name__": "__main__"}
        for index, cell in enumerate(notebook["cells"], 1):
            if cell["cell_type"] == "code":
                exec(compile("".join(cell["source"]), f"{script}:cell {index}", "exec"), namespace)
    except SystemExit as exit_request:
        if exit_request.code not in (None, 0):
            raise RuntimeError(f"{script.name} exited with status {exit_request.code}") from exit_request
    finally:
        sys.argv = previous_argv
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
                if lesson.name.endswith("_python_warmup"):
                    print(f"SKIP run        {prefix_of(lesson)}_learning.ipynb (student exercise)")
                    continue
                prefix = prefix_of(lesson)
                for kind in ("learning", "solutions"):
                    script = lesson / f"{prefix}_{kind}.ipynb"
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
