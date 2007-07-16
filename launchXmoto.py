import logging, log
from xmotoExtension import XmotoExtension, getInkscapeExtensionsDir
from svg2lvl import svg2lvl
from os.path import join, isfile
from os import execl, execlp
import sys

class launchXmoto(XmotoExtension):
    def __init__(self):
        XmotoExtension.__init__(self)
        self.OptionParser.add_option("--xmoto",   type="string", dest="xmoto",   help="xmoto executable")
        self.OptionParser.add_option("--dummy",   type="string", dest="dummy",   help="dummy text")

    # we don't want to update the svg.
    def parse(self):
        pass
    def getposinlayer(self):
        pass
    def getselected(self):
        pass
    def getdocids(self):
        pass

    def effect(self):
        # check that the xmoto executable is present
        givenXmotoPresent = True
        if not isfile(self.options.xmoto):
            givenXmotoPresent = False
            
        # export in lvl
        lvlfileName = join(getInkscapeExtensionsDir(), 'last.lvl')
        svg2lvl(sys.argv[-1], lvlfileName)

        # launch it in xmoto
        if givenXmotoPresent == True:
            execl(self.options.xmoto, 'xmoto', lvlfileName)
        else:
            try:
                execlp('xmoto', 'xmoto', lvlfileName)
            except:
                raise Exception("The xmoto executable is present neither in the given location (%s) nor in the PATH" % self.options.xmoto)

    def output(self):
        pass


e = launchXmoto()
e.affect()