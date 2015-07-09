#!/usr/bin/env python
import re
import sys

def slugify(value):
    """
    http://stackoverflow.com/questions/5574042/string-slugification-in-python
    Converts to lowercase, removes non-word characters (alphanumerics and
    underscores) and converts spaces to hyphens. Also strips leading and
    trailing whitespace.
    """
    value = re.sub('[^\w\s-]', '', value).strip().lower()
    return re.sub('[-\s]+', '-', value)


text = " ".join(sys.argv[1:])
replacements = [
  ['bug-', 'bug/'],
  ['feature-', 'feature/'],
  ['fix-', 'fix/']
]
text = slugify(text)
for r in replacements:
  text = text.replace(r[0], r[1])
print(text)
sys.exit()
