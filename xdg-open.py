#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
XDG-OPEN Replacement

This new xdg-open python scripts replaces the old /usr/bin/xdg-open

Features:
    1. Easy to customize and modify
    2. Support to new protocols like smb://, ftp://, ssh://, telnet://, file://,

    3. Supports Special Protocols Like
    Geo Location geo://<latitude>,<longitude>,z=<zoom>,t=<map type: m,k,h,p>
    Executable   command://<path to executable>
    Deep Web     tor://<url.onion>
    Jar file     jar:<path-to-jar-file>

    4. All configuration can be done by editing /etc/xdgrc

"""


import os
import sys
import re

from subprocess import call, Popen

HOME = os.path.expanduser('~')
userconfig = os.path.join(HOME, '.xdgrc')


handlers_conf = open('/etc/xdgrc','r').read()
_handlers = re.findall('(.*)\s*:\s*(.*)\s*', handlers_conf)
apps = [a[0] for a in _handlers]
cmd  = [a[1] for a in _handlers]
handlers = dict(zip(apps, cmd))
#print handlers



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

# match geo://8.003809,34.88922,z=20,t=h
# Latitude: 8.003809
# Longitude: 34.89922
# zoom: 20 (maximum)
# Hibryd map: h
geo_url = re.compile("geo:(?://)?([-+]?\d*\.\d+|\d+),([-+]?\d*\.\d+|\d+)(?:,z=(\d+))?(?:,t=([m|k|h|p]))?")


spreadsheet_mimes = "application/wps-office.et;application/wps-office.ett;application/wps-office.xls;application/wps-office.xlt;application/vnd.ms-excel;application/msexcel;application/x-msexcel;application/wps-office.xlsx;application/wps-office.xltx"
wiriter_mimes = "application/wps-office.wps;application/wps-office.wpt;application/wps-office.doc;application/wps-office.dot;application/vnd.ms-word;application/msword;application/x-msword;application/msword-template;application/wps-office.docx;application/wps-office.dotx;application/rtf"
presentation_mimes = "application/wps-office.dps;application/wps-office.dpt;application/wps-office.ppt;application/wps-office.pot;application/vnd.ms-powerpoint;application/vnd.mspowerpoint;application/mspowerpoint;application/powerpoint;application/x-mspowerpoint;application/wps-office.pptx;application/wps-office.potx"

spreadsheet_mimes =  spreadsheet_mimes.split(';')
wiriter_mimes = wiriter_mimes.split(';')
presentation_mimes = presentation_mimes.split(';')



def filehandler(filename):

    import magic

    compressed_format = ('.tgz', '.gz', '.bz2', '.tar', '.tar.gz', '.tar.bz2', '.zip', '.rar', '.7z', '.jar')

    magic = magic.from_file(filename, mime=True)

    #magic.from_file("win7-desktop.py", mime=True)

    #basename = os.path.basename(filename)

    if os.path.isdir(filename):
        Popen([handlers['FILEMANAGER'], filename])


    # BINARY EXECUTABLES
    #------------------------------
    elif filename.endswith('.exe'):
        Popen(['wine', filename])

    elif filename.endswith('.msi'):
        Popen(['msiexec', '/i', filename])

    elif filename.endswith('.egg'):
        Popen(['python', filename])

    elif filename.endswith('.deb'):
        Popen(['gdebi', filename])

    elif magic == 'application/pdf':
        Popen([handlers['PDF'], filename])

    elif magic ==  "text/html":
        Popen([handlers['BROWSER'], filename])

    #  TEXT FILE
    #--------------------------------
    elif magic.startswith('text'):
        Popen([handlers['EDITOR'], filename])

    # MULTIMEDIA
    #-------------------------------------
    elif magic.startswith('image'):
        Popen([handlers['IMAGE'], filename])

    elif magic.startswith('video'):
        Popen([handlers['VIDEO'], filename])

    elif magic.startswith('audio'):
        Popen([handlers['AUDIO'], filename])

    # OFFICE DOCUMENTS, doc, presentation, spreadsheet
    #--------------------------------------
    elif magic in spreadsheet_mimes:
        Popen([handlers['SPREADSHEET'], filename])

    elif magic in wiriter_mimes:
        Popen([handlers['WRITER'], filename])

    elif magic in presentation_mimes:
        Popen([handlers['PRESENTATION'], filename])


# ONION URL
if onion_url:
    print onion_url
    url = onion_url[0][1]
    url = re.sub('.onion', '.tor2web.org', url)
    Popen([handlers['BROWSER'], url])
elif re.match('tor://.*', uri):
    url = uri.split('tor://')[1]
    url = re.sub('.onion', '.tor2web.org', url)
    Popen([handlers['BROWSER'], url])

# GEOLOCATION
elif geo_url.match(uri):

    lat, lon, zoom, map_type = geo_url.findall(uri)[0]
    if zoom:
        z= "z=%s&" % zoom
    else:
        z= ""

    if map_type:
        t= "t=%s&" % map_type
    else:
        t= ""

    url = "https://www.google.com/local?%s%sq=%s,%s" % (z, t, lat, lon)
    Popen([handlers['BROWSER'], url])

#Execute Command
elif re.match("command://.*", uri):
    cmd = uri.split('command://')[1]
    cmd = cmd.split()
    Popen(cmd)

#JAR FILE
elif re.match('jar:.*', uri):
    Popen(['java', '-jar', uri.split('jar:')[1]])

# WEB PAGE
elif re.match('http://.*', uri) or re.match('www\..*', uri):
    Popen([handlers['BROWSER'], uri])

# MAGNET LINK
elif torrent_url:
    Popen([handlers['TORRENT'], uri])

# SSH
elif re.match('ssh://.*', uri):
    Popen([handlers['SSH'], uri.split('ssh://')[1]])

# TELNET
elif re.match('telnet://.*', uri):
    Popen(['telnet', uri])


# SFTP
elif re.match('sftp://.*', uri):
    Popen([handlers['SFTP'], uri])

#FTP
elif re.match('ftp://.*', uri):
    Popen([handlers['FTP'], uri])

#SMB
elif re.match('smb://.*', uri):
    Popen([handlers['SMB'], uri])

elif re.match('\\.*', uri):
    Popen([handlers['SMB'], uri])


#MAILTO
elif re.match('mailto://.*', uri):
    Popen([handlers['MAILTO'], uri])

elif file_url:
    filehandler(file_url)

else:
    print "File Handler"
    filehandler(uri)
