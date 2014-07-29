xdg-open
========

A python xdg open python script replacement easy to change. Supports new uris like geo://(geo location), sftp://, smb://, tor://(deep web), command://, ssh://, telnet://, 

XDG-OPEN Replacement

This new xdg-open python scripts replaces the old /usr/bin/xdg-open

#Features:

1. Easy to customize and modify

2. Support to new protocols like smb://, ftp://, ssh://, telnet://, file://,

3. Supports Special Protocols Like

~~~~~~~
      Geo Location geo://<latitude>,<longitude>,z=<zoom>,t=<map type: m,k,h,p>
      
      Executable   command://<path to executable>
      
      Deep Web     tor://<url.onion>
      
      Jar file     jar:[path-to-jar-file]

4. All configuration can be done by editing /etc/xdgrc


#Testing

------------------
Open Directory
  xdg-open  file:///home

Open File
  xdg-open  file:///home/tux/.bashrc

#Install
