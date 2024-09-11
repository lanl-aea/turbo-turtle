import os


try:
    import cubit
except ImportError:
    import sys
    sys.modules["cubit"] = type(sys)("cubit")


display = os.environ.get("DISPLAY")
if not display:
    missing_display = True
else:
    missing_display = False
