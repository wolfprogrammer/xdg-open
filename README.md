xdg-open
========

\#xdg-open  \#linux \#tor \#geolocation \#geo

A python xdg open python script replacement easy to change. Supports new uris like geo://(geo location), sftp://, smb://, tor://(deep web), command://, ssh://, telnet://, 

XDG-OPEN Replacement

This new xdg-open python scripts replaces the old /usr/bin/xdg-open

See also: https://wiki.archlinux.org/index.php/xdg-open

#Features:

* Easy to customize and modify

* Support to new protocols like smb://, ftp://, ssh://, telnet://, file://,

* Supports Special Protocols Like

* All configuration can be done by editing /etc/xdgrc

#Install

```
git clone https://github.com/wolfprogrammer/xdg-open.git
cd xdg-open
cp /usr/bin/xdg-open xdg-open.backup
sudo ./install.sh

```


#Testing


Open Directory
```
xdg-open  file:///home
```

Open File
```
xdg-open  file:///home/tux/.bashrc
```

Geo Location
```
Open latitude and longitude in the browser
xdg-open geo://[latitude],[longitude],z=[zoom],t=[map type: m,k,h,p]
```

Executable   
```
xdg-open command://[path to executable]
```

Deep Web 
```
xdg-open tor://[ONION URL]
```

Jar file     
```
xdg-open jar:[path-to-jar-file]
```

