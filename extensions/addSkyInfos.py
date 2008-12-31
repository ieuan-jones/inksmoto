from xmotoExtensionTkinter import XmotoExtTkLevel, XmotoBitmap, XmotoScale, XmotoCheckBox
from xmotoTools import createIfAbsent, getValue, alphabeticSortOfKeys
import logging, log
import Tkinter
from listAvailableElements import textures

class AddSkyInfos(XmotoExtTkLevel):
    def __init__(self):
        XmotoExtTkLevel.__init__(self)

    def updateLabelData(self):
        def removeUnusedDatas(dataKeys):
            for key in dataKeys:
                if key in self.label['sky']:
                    del self.label['sky'][key]

        self.label['sky']['tex'] = self.tex.get()

        if self.useParams.get() == 1:
            self.label['sky']['use_params'] = 'true'
            self.label['sky']['zoom']       = self.zoom.get()
            self.label['sky']['offset']     = self.offset.get()
            self.label['sky']['color_r']    = self.color_r.get()
            self.label['sky']['color_g']    = self.color_g.get()
            self.label['sky']['color_b']    = self.color_b.get()
            self.label['sky']['color_a']    = self.color_a.get()
        else:
            removeUnusedDatas(['zoom', 'offset', 'color_r', 'color_g', 'color_b', 'color_a'])
            self.label['sky']['use_params'] = 'false'

        if self.useDrift.get() == 1:
            self.label['sky']['drifted']      = 'true'
            self.label['sky']['driftZoom']    = self.driftZoom.get()
            self.label['sky']['driftColor_r'] = self.driftColor_r.get()
            self.label['sky']['driftColor_g'] = self.driftColor_g.get()
            self.label['sky']['driftColor_b'] = self.driftColor_b.get()
            self.label['sky']['driftColor_a'] = self.driftColor_a.get()
        else:
            removeUnusedDatas(['driftZoom', 'driftColor_r', 'driftColor_g', 'driftColor_b', 'driftColor_a'])
            self.label['sky']['drifted'] = 'false'

    def createWindow(self):
        createIfAbsent(self.label, 'sky')

        self.defineWindowHeader('Sky properties')

        bitmapSize = self.getBitmapSizeDependingOnScreenResolution()

        self.defineLabel(self.frame, "sky texture:")
        defaultTexture    = getValue(self.label, 'sky', 'tex', default='_None_')
        self.tex          = XmotoBitmap(self.frame, textures[defaultTexture]['file'], defaultTexture, self.textureSelectionWindow, buttonName="texture", size=bitmapSize)
        self.useParams    = XmotoCheckBox(self.frame, getValue(self.label, 'sky', 'use_params'), text='Use parameters', command=self.paramsCallback)
        self.zoom         = XmotoScale(self.frame, getValue(self.label, 'sky', 'zoom'),         label='zoom:',              from_=0.1,  to=10,  resolution=0.1,   default=2)
        self.offset       = XmotoScale(self.frame, getValue(self.label, 'sky', 'offset'),       label='offset:',            from_=0.01, to=1.0, resolution=0.005, default=0.015)
        self.color_r      = XmotoScale(self.frame, getValue(self.label, 'sky', 'color_r'),      label='red color:',         from_=0,    to=255, resolution=1,     default=255)
        self.color_g      = XmotoScale(self.frame, getValue(self.label, 'sky', 'color_g'),      label='green color:',       from_=0,    to=255, resolution=1,     default=255)
        self.color_b      = XmotoScale(self.frame, getValue(self.label, 'sky', 'color_b'),      label='blue color:',        from_=0,    to=255, resolution=1,     default=255)
        self.color_a      = XmotoScale(self.frame, getValue(self.label, 'sky', 'color_a'),      label='alpha color:',       from_=0,    to=255, resolution=1,     default=255)
        self.useDrift     = XmotoCheckBox(self.frame, getValue(self.label, 'sky', 'drifted'), text='Drifted sky:', command=self.driftCallback)
        self.driftZoom    = XmotoScale(self.frame, getValue(self.label, 'sky', 'driftZoom'),    label='drift zoom:',        from_=0.1,  to=5,   resolution=0.1,   default=2)
        self.driftColor_r = XmotoScale(self.frame, getValue(self.label, 'sky', 'driftColor_r'), label='drift red color:',   from_=0,    to=255, resolution=1,     default=255)
        self.driftColor_g = XmotoScale(self.frame, getValue(self.label, 'sky', 'driftColor_g'), label='drift green color:', from_=0,    to=255, resolution=1,     default=255)
        self.driftColor_b = XmotoScale(self.frame, getValue(self.label, 'sky', 'driftColor_b'), label='drift blue color:',  from_=0,    to=255, resolution=1,     default=255)
        self.driftColor_a = XmotoScale(self.frame, getValue(self.label, 'sky', 'driftColor_a'), label='drift alpha color:', from_=0,    to=255, resolution=1,     default=255)

        self.paramsCallback()
        self.driftCallback()

    def bitmapSelectionWindowHook(self, imgName, buttonName):
        values = self.tex.update(imgName, textures)

    def paramsCallback(self):
        widgets = [self.zoom, self.offset, self.color_r, self.color_g,
                   self.color_b, self.color_a]
        if self.useParams.get() == 1:
            for widget in widgets:
                widget.show()
        else:
            for widget in widgets:
                widget.hide()

    def driftCallback(self):
        widgets = [self.driftZoom, self.driftColor_r, self.driftColor_g,
                   self.driftColor_b, self.driftColor_a]
        if self.useDrift.get() == 1:
            for widget in widgets:
                widget.show()
        else:
            for widget in widgets:
                widget.hide()

e = AddSkyInfos()
e.affect()
