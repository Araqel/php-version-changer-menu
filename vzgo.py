import gi
import os
import signal
import json
import string
import subprocess
import re

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
gi.require_version('Notify', '0.7')

from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Notify as notify
from subprocess import call

APPINDICATOR_ID = 'Araqels_PHP_Version_Changer_For_Ubuntu'


def main():
    global indicator
    global dir_path
    dir_path = os.path.dirname(os.path.realpath(__file__))

    current_version= getPhpVersion()
    indicator = appindicator.Indicator.new(APPINDICATOR_ID, dir_path+'/icons/php'+current_version+'.png',
                                          appindicator.IndicatorCategory.SYSTEM_SERVICES)
   
    indicator.set_label('PHP '+current_version,APPINDICATOR_ID)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    notify.init(APPINDICATOR_ID)
    gtk.main()



def build_menu():
    versions=fetchVersions()
    menu = gtk.Menu()
    for version in versions:
        menu_icon = gtk.Image()
        menu_icon.set_from_file(dir_path+'/icons/php'+version+'.png')
  
        menu_item=gtk.ImageMenuItem(version)
        menu_item.set_always_show_image(True)
        menu_item.set_image(menu_icon)

        menu_item.connect('activate',changePhpVersion,version)
        menu.append(menu_item)

    menu.show_all()
    return menu


def fetchVersions():
    pipe = subprocess.Popen("ls /etc/php", shell=True, stdout=subprocess.PIPE)
    output = pipe.stdout
    versions=[]
    for line in output.read().splitlines():
        versions.append(line.decode('utf-8'))

    return versions


def changePhpVersion(menuitem,version):
    call(['gksudo',dir_path+'/change_php_version.sh '+version])
    current_version=getPhpVersion()
    indicator.set_label("PHP " + current_version, APPINDICATOR_ID)
    indicator.set_icon(dir_path+'/icons/php'+current_version+'.png')



def getPhpVersion():
    pipe = subprocess.Popen("php -v | grep -i '^php'", shell=True, stdout=subprocess.PIPE)
    output = pipe.stdout
    text=output.readline().decode('utf-8')

    return re.search('([0-9].[0-9])',text).group(1)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
