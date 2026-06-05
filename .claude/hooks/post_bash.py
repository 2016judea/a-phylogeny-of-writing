import sys, json
try:
    json.load(sys.stdin)
except Exception:
    pass