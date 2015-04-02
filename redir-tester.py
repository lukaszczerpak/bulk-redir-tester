#!/usr/bin/env python

import sys, csv
import redir_lib

data = open(sys.argv[1]).readlines()
redirs = csv.DictReader(data,
                        delimiter=' ', skipinitialspace=True,
                        fieldnames=['status', 'sourceURL', 'targetURL'])

realHostname = sys.argv[2]

for r in redirs:

    sourceURL = r['sourceURL']
    errors = redir_lib.checkRedirect(r, realHostname)

    if len(errors) > 0:
        print 'ERROR on %s\n%s' % (sourceURL, '\n'.join(errors))
    else:
        print 'OK: %s' % (sourceURL)

    print '-' * 120
