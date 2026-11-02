def main():
    import runpy
    import os
    import sys

    platformer_path = os.path.join(os.path.dirname(__file__), "..", "..", "platformer")
    sys.path.insert(0, os.path.abspath(platformer_path))
    runpy.run_module("main", run_name="__main__", alter_sys=True)
