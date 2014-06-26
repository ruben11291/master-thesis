#!/bin/sh

icegridadmin -e "aplication add cfg/HelloApp.xml" --Ice.Config=cfg/locator.cfg
icestormadmin -e "create hello" --Ice.Config=cfg/icestorm.cfg

