import gi
import os
import signal
import json
import string
import subprocess
import re

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')

from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Notify as notify
from subprocess import call

APPINDICATOR_ID = 'myappindicator'


def main():
    global indicator
    indicator = appindicator.Indicator.new(APPINDICATOR_ID, os.path.abspath('php.png'),
                                          appindicator.IndicatorCategory.SYSTEM_SERVICES)
   
    current_version= getPhpVersion()
    indicator.set_label(current_version,APPINDICATOR_ID)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    notify.init(APPINDICATOR_ID)
    gtk.main()



def build_menu():
    versions=fetchVersions()
    menu = gtk.Menu()
    for version in versions:
        menu_item=gtk.MenuItem(version)
        menu_item.connect('activate',changePhpVersion,version)
        menu.append(menu_item)


    item_quit = gtk.MenuItem('Quit')
   # item_quit.connect('activate', quit)
    menu.append(item_quit)
    menu.show_all()
    return menu


def fetchVersions():
    # aaa=call(['ls','/etc/php'])
    # return aaa[0]
    pipe = subprocess.Popen("ls /etc/php", shell=True, stdout=subprocess.PIPE)
    output = pipe.stdout
    versions=[]
    for line in output.read().splitlines():
        versions.append(line.decode('utf-8'))

    return versions


def changePhpVersion(menuitem,version):
    call(['gksudo','./change_php_version.sh '+version])	
    indicator.set_label("PHP "+version,APPINDICATOR_ID)


def quit(_):
    notify.uninit()
    gtk.main_quit()

def getPhpVersion():
    pipe = subprocess.Popen("php -v | grep -i '^php'", shell=True, stdout=subprocess.PIPE)
    output = pipe.stdout
    text=output.readline().decode('utf-8')

    return re.search('(PHP [0-9].[0-9])',text).group(1)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
