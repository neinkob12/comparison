"""Vertont mehrere Videos parallel: python3 scripts/build_all.py 2 50"""
import sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, __import__("os").path.dirname(__file__))
import build

ids = [f"a{n:02d}" for n in range(int(sys.argv[1]), int(sys.argv[2]) + 1)]
with ThreadPoolExecutor(4) as ex:
    for f in [ex.submit(build.build, i) for i in ids]:
        f.result()
