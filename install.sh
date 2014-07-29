#!/bin/bash

cp /usr/bin/xdg-open xdg-open.backup
chmod +x xdg-open.py
sudo cp xdg-open.py  /usr/bin/xdg-open
sudo cp xdgrc /etc
