import json
import argparse
from macapptree import get_app_bundle, get_tree

from Quartz import (
    CGWindowListCopyWindowInfo,
    kCGWindowListOptionOnScreenOnly,
    kCGNullWindowID,
    kCGWindowOwnerName,
    kCGWindowBounds
)

INVALID_WINDOWS=['Window Server', 'Notification Center']
options = kCGWindowListOptionOnScreenOnly
windowList = CGWindowListCopyWindowInfo(options, kCGNullWindowID)
# Convert windowList to a list of Python dictionaries
app_names = []
for window in windowList:
  real = False
  for key, value in window.items():
    if key == kCGWindowBounds:
      if value["Y"] > 0:
        real = True
  for key, value in window.items():
    if key == kCGWindowOwnerName and real == True:
      if value not in INVALID_WINDOWS:
        app_names.append(value)

out = []
for app in app_names:
  bundle = get_app_bundle(app)
  out.append({
    'name': app,
    'role': 'application',
    'description': '',
    'value': '',
    'bbox': {'x': 0, 'y': 0, 'width': 0, 'height': 0},
    'children': get_tree(bundle)
  })

parser = argparse.ArgumentParser(description='Extract accessibility tree from macOS applications')
parser.add_argument('-o', '--out', help='Output file path (defaults to stdout)')
args = parser.parse_args()

json_output = json.dumps(out)

if args.out:
    with open(args.out, 'w') as f:
        f.write(json_output)
    print(f"Accessibility tree exported to {args.out}")
else:
    print(json_output)
