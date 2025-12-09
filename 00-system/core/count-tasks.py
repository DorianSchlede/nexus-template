import re
from pathlib import Path

file_path = Path("02-projects/00-onboarding/00-define-goals/01-planning/steps.md")
content = file_path.read_text(encoding='utf-8')

tasks = re.findall(r'- \[([ xX])\]', content)
checked = sum(1 for t in tasks if t.lower() == 'x')
unchecked = sum(1 for t in tasks if t == ' ')

print(f"Total tasks: {len(tasks)}")
print(f"Checked: {checked}")
print(f"Unchecked: {unchecked}")
