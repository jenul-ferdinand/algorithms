import argparse
import re
import unittest


if __name__ == "__main__":

    p = argparse.ArgumentParser()
    p.add_argument(
        "task",
        help=(
            "The task number you'd like to run. "
            "Leave blank for all tasks.\n\n"
            "Example: local_run_tests.py 3\n"
            "Runs the tests with @number('3.x')."
        ),
        default="",
        nargs="?",
    )
    args = p.parse_args()

    while args.task == '':
        try:
            task = input("Enter task [1 - 6], leave blank to run all tests: ")
            if task == '':
                break
            if 1 <= int(task) <= 6:
                args.task = task
        except ValueError:
            pass

    suite = unittest.defaultTestLoader.discover('.')
    for s in suite:
        for t in s:
            if "FailedTest" in str(type(t)):
                continue
            marked_remove = set()
            for t2 in t:
                func = getattr(t2, t2._testMethodName)
                if args.task and not re.match(rf"^{args.task}\.", getattr(func, "__number__", "")):
                    marked_remove.add(t2)
            for t2 in marked_remove:
                t._tests.remove(t2)

    runner = unittest.runner.TextTestRunner(verbosity=2)
    runner.run(suite)
