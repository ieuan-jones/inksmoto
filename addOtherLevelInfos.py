from xmotoExtensionTkinter import XmotoExtensionTkinter
import logging, log
import Tkinter
import xml.dom.Element
import xml.dom.Text
from inkex   import NSS

class AddOtherLevelInfos(XmotoExtensionTkinter):
    def __init__(self):
        XmotoExtensionTkinter.__init__(self)

    def updateLabelData(self):
        for name, value in self.remplacement.iteritems():
            self.label['remplacement'][name] = value.get(Tkinter.ACTIVE)

        self.label['level']['music'] = self.music.get(Tkinter.ACTIVE)

    def effect(self):
        self.getMetaData()
        if not self.label.has_key('level'):
            self.label['level'] = {}
        if not self.label.has_key('remplacement'):
            self.label['remplacement'] = {}

        root = Tkinter.Tk()
        root.title('Other level properties')
        self.frame = Tkinter.Frame(root)
        self.frame.pack()

        from listAvailableElements import sprites, musics

        self.remplacement = {}
        for name in ['Strawberry', 'Wrecker', 'Flower', 'PickUpStrawberry']:
            self.remplacement[name] = self.defineListbox('remplacement', name=name, label='%s remplacement' % name, items=['None']+sprites)

        self.music = self.defineListbox('level', name='music', label='Level music', items=['None']+musics)

        self.defineOkCancelButtons()
        root.mainloop()

e = AddOtherLevelInfos()
e.affect()
