import os


display = os.environ.get("DISPLAY")
if not display:
    missing_display = True
else:
    missing_display = False
