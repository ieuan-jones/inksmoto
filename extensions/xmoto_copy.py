from inkex import addNS
from xmotoExtension import XmExt
import logging, log

class XmotoCopy(XmExt):
    def __init__(self):
        XmExt.__init__(self)

    def effectHook(self):
        if len(self.selected) != 1:
            log.outMsg("You have to only select the object whose you want to copy the Xmoto parameters.")
            return False

        node = self.selected[self.options.ids[0]]
        label = node.get(addNS('xmoto_label', 'xmoto'))

        if label is None:
            log.outMsg("The selected object has no Xmoto properties to copy.")
            return False

        (descriptionNode, metadata) = self.getAndCreateMetadata()
        descriptionNode.set(addNS('saved_xmoto_label', 'xmoto'), label)

        return False

if __name__ == "__main__":
    e = XmotoCopy()
    e.affect()
