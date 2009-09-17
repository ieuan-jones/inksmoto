#!/bin/python
"""
Copyright (C) 2006,2009 Emmanuel Gorse, e.gorse@gmail.com

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
"""

import log, logging
import sys

try:
    import gtk
    import gtk.glade
except:
    log.outMsg("You need to install PyGtk")
    sys.exit(1)

from os.path import join
from xmotoTools import getSystemDir, getExistingImageFullPath
from xmotoTools import alphabeticSortOfKeys
from availableElements import AvailableElements

TEXTURES = AvailableElements()['TEXTURES']
EDGETEXTURES = AvailableElements()['EDGETEXTURES']
SPRITES = AvailableElements()['SPRITES']
PARTICLESOURCES = AvailableElements()['PARTICLESOURCES']

EDGETEXTURES['_None_'] = {'file':'none.png'}
TEXTURES['_None_'] = {'file':'none.png'}
SPRITES['_None_'] = {'file':'none.png'}

def quit(widget=None):
    """ the widget param is present when called from a gtk signal
    """
    gtk.main_quit()

def mainLoop():
    gtk.main()

def errorMessageBox(msg):
    gtk.MessageDialog(parent=None, flags=gtk.DIALOG_MODAL,
                      type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE,
                      message_format=msg).run()

def createWindow(gladeFile, windowName):
    return gtk.glade.XML(join(getSystemDir(), 'glade', gladeFile),
                         windowName)

def addImgToBtn(button, label, imgName, bitmapDict):
    imgFile = bitmapDict[imgName]['file']
    imgFullFile = getExistingImageFullPath(imgFile)

    if imgFullFile is None:
        imgFile = '__missing__.png'
        imgFullFile = getExistingImageFullPath(imgFile)

    img = gtk.Image()
    img.set_from_file(imgFullFile)
    button.set_image(img)
    label.set_text(imgName)

def resetColor(button):
    button.set_color(gtk.gdk.color_parse('white'))
    button.set_alpha(65535)

class bitmapSelectWindow:
    def __init__(self, title, bitmaps):
        self.selectedImage = None

        wTree = createWindow('bitmapSelection.glade', 'bitmapSelection')
        self.window = wTree.get_widget('bitmapSelection')
        self.window.set_title(title)
        self.window.connect("destroy", gtk.main_quit)

        self.keys = alphabeticSortOfKeys(bitmaps.keys())

        store = gtk.ListStore(str, gtk.gdk.Pixbuf)
        store.set_sort_column_id(0, gtk.SORT_ASCENDING)
        store.clear()

        for name in self.keys:
            try:
                # skeep the __biker__.png image used for PlayerStart
                if bitmaps[name]['file'][0:2] == '__':
                    continue

                imgFile = bitmaps[name]['file']
                imgFullFile = getExistingImageFullPath(imgFile)
                if imgFullFile is None:
                    imgFile = '__missing__.png'
                    imgFullFile = getExistingImageFullPath(imgFile)
                pixBuf = gtk.gdk.pixbuf_new_from_file(imgFullFile)

                store.append([name, pixBuf])

            except Exception, e:
                logging.info("Can't create bitmap for %s\n%s" % (name, e))
                store.append([name, None])

        iconView = wTree.get_widget('bitmapsView')
        iconView.set_model(store)
        iconView.set_text_column(0)
        iconView.set_pixbuf_column(1)
        iconView.connect("item-activated", self.bitmapSelected)

    def run(self):
        self.window.show_all()
        gtk.main()
        return self.selectedImage

    def bitmapSelected(self, iconView, imageIdx):
        self.selectedImage = self.keys[imageIdx[0]+1]
        self.window.destroy()
        gtk.main_quit()
