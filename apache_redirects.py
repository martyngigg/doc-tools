"""
Generate an apache rewrite map in a simple text format
that maps the location of old algorithm docs to their new locations.

See http://httpd.apache.org/docs/current/rewrite/rewritemap.html

The output is sent to stdout.
"""
from __future__ import print_function
try:
    import mantid
except ImportError:
    import sys
    print("Cannot import mantid. Make sure PYTHONPATH points at Mantid",
          sys.stderr)
    sys.exit(1)

from mantid.api import AlgorithmFactory

################################################################################

# Redirect destination
DOCS_URL = "http://docs.mantidproject.org/"
ALGS_URL = DOCS_URL + "algorithms/"

HEADER = \
"""#
# THIS FILE WAS AUTO-GENERATED FROM A SCRIPT: apache_redirects.py
#
# See https://github.com/martyngigg/doc-tools/edit/master/apache_redirects.py
"""

# Format the file in to two columns by finding the longest name
algs = AlgorithmFactory.getRegisteredAlgorithms(True)
longest_name = -1
for name in iter(algs):
    if len(name) > longest_name:
        longest_name = len(name)
#
longest_uri = longest_name + 1 # extra forward slash in final text
col_width = longest_uri + 5 # pad with five spaces
sorted_algs = sorted(algs)

print(HEADER)
print
for name in iter(sorted_algs):
    # Redirect goes to highest version
    versions = algs[name]
    versions = sorted(versions)
    highest_version = versions[-1]
    uri = "/" + name
    uri = uri.ljust(col_width)
    alg_url = "%s%s-v%d.html" % (ALGS_URL, name, highest_version)
    line = "%s%s" % (uri, alg_url)
    print(line)
