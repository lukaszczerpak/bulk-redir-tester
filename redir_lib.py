#!/usr/bin/env python

import re, httplib

def escapePath(url):
    url = url.replace('&', '&amp;')
    url = url.replace('-', r'\-')
    url = url.replace('+', r'\+')
    url = url.replace('?', r'\?')
    return url


def checkRedirect(r, realHostname):
    sourceURL = r['sourceURL']
    expectedTargetURL = r['targetURL']
    redirCode = int(r['status'])

    errors = []

    match = re.match('^(http|https)://([a-zA-Z0-9\-\.]+)(:([0-9]+))?(/.*)$', sourceURL)
    proto = match.group(1)
    hostname = match.group(2)
    path = match.group(5)

    if proto == 'https':
        port = 443
    else:
        port = 80

    if match.group(3)<>None:
        port = match.group(4)

    if proto == 'https':
        conn = httplib.HTTPSConnection(realHostname, port)
    else:
        conn = httplib.HTTPConnection(realHostname, port)

    headers = {'Host': hostname}
    conn.request('GET', path, None, headers)
    response = conn.getresponse()
    internalRedir = True if response.getheader('Server') == 'AkamaiGHost' else False

    if response.status != redirCode:
        errors.append('Incorrect response code:\n\texpected: %d\n\tgot: %d' % (redirCode, response.status))

    if response.status in (301, 302):
        targetURL = response.getheader('Location')
        if targetURL != expectedTargetURL:
            errors.append('Invalid target URL:\n\texpected: %s\n\tgot: %s' % (expectedTargetURL, targetURL))

    return errors


def escapeUrl(url):
    url = url.replace('&', '&amp;')
    return url
