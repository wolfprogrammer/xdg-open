#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
http://en.wikipedia.org/wiki/URI_scheme

sftp://[<user>[;fingerprint=<host-key fingerprint>]@]<host>[:<port>]/<path>/<file>


WINDOWS SMB/ SAMBA

    IETF Draft 	smb://[<user>@]<host>[:<port>][/[<path>]][?<param1>=<value1>[;<param2>=<value2>]] or
    smb://[<user>@]<workgroup>[:<port>][/] or
    smb://[[<domain>;]<username>[:<password>]@]<server>[:<port>][/[<share>[/[<path>]]][?[<param>=<value>[<param2>=<value2>[...]]]]][5]
    example:
    smb://workgroup;user:password@server/share/folder/file.txt

TELEPHONE Number
tel:<phonenumber>


telnet://<user>:<password>@<host>[:<port>/]

rsync://<host>[:<port>]/<path>


feed:<absolute_uri> or
feed://<hierarchical part>

examples:
feed://example.com/rss.xml
feed:https://example.com/rss.xml


  apt:<package name>

GEO URI
geo:37.786971,-122.399677
http://developer.android.com/guide/components/intents-common.html
http://geosms.wordpress.com/


"""


import os
import sys
import re

from subprocess import call, Popen

HOME = os.path.expanduser('~')
userconfig = os.path.join(HOME, '.xdgrc')


handlers_conf = open('xdgrc','r').read()
_handlers = re.findall('(.*)\s*:\s*(.*)\s*', handlers_conf)
apps = [a[0] for a in _handlers]
cmd  = [a[1] for a in _handlers]
handlers = dict(zip(apps, cmd))
print handlers



if len(sys.argv) < 2:
    sys.exit(0)

uri = sys.argv[1]


def test_pattern(pattern, txt):
    import re

    q = re.findall(pattern, txt)
    if not q:
        return False
    else:
        return q[0].strip()
# magnet:?xt=urn:btih:95113ea2cfbf75b05709209d2f83502f69d736be&dn=Tor+Onion+Network+-+Preconfigured+Hidden+Service+%5BMac+OSX%5D&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80&tr=udp%3A%2F%2Ftracker.publicbt.com%3A80&tr=udp%3A%2F%2Ftracker.istole.it%3A6969&tr=udp%3A%2F%2Fopen.demonii.com%3A1337

http_url     = test_pattern('http://(.*)', uri)
https_url     = test_pattern('https://(.*)', uri)
file_url     = test_pattern('file://(.*)', uri)
torrent_url  = test_pattern('magnet:(.*)', uri)
ftp_url      = test_pattern('ftp://(.*)', uri)
sftp_url     = test_pattern('sftp://(.*)', uri)
onion_url    = re.findall("(http://|https://)(.*\.onion.*)", uri)

print "\n\n"

def filehandler(filename):
    pass

# ONION URL
if onion_url:
    print onion_url
    url = onion_url[0][1]
    url = re.sub('.onion', '.tor2web.org', url)
    Popen([handlers['BROWSER'], url])

# GEOLOCATION
elif re.match("geo:(.*),(.*)", uri):

    lat, lon = re.findall("geo:(.*),(.*)", uri)[0]
    url = "https://www.google.com/local?q=%s,%s" % (lat, lon)
    Popen([handlers['BROWSER'], url])

    print lat
    print lon

# WEB PAGE
elif re.match('http://.*', uri) or re.match('www\..*', uri):
    Popen([handlers['BROWSER'], uri])

# MAGNET LINK
elif torrent_url:
    Popen([handlers['TORRENT'], uri])

# SSH
elif re.match('ssh://.*', uri):
    Popen([handlers['SSH'], uri.split('ssh://')[1]])

# SFTP
elif re.match('sftp://.*', uri):
    Popen([handlers['SFTP'], uri])

#FTP
elif re.match('ftp://.*', uri):
    Popen([handlers['FTP'], uri])

#SMB
elif re.match('smb://.*', uri):
    Popen([handlers['SMB'], uri])


elif file_url:
    filehandler(file_url)

