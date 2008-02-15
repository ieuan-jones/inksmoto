from xmotoExtension import XmotoExtension, getInkscapeExtensionsDir
from inkex import addNS, NSS
from lxml import etree
from lxml.etree import Element
from os.path import join
import Tkinter
import Image, ImageTk
import Tix
import tkFileDialog
import logging, log

class XmotoExtensionTkinter(XmotoExtension):
    """ use for extensions with their own window made with tkinter
    """
    def __init__(self):
        XmotoExtension.__init__(self)

    def getMetaData(self):
        self.labelValue  = ''
	self.description = None
        descriptions = self.document.xpath('//dc:description', NSS)
        if descriptions is not None and len(descriptions) > 0:
            self.description = descriptions[0]
	    self.labelValue = self.description.text

        self.parseLabel(self.labelValue)

    def setMetaData(self):
        self.updateLabelData()

        self.frame.quit()

        self.unparseLabel()

        if self.description is not None:
            self.description.text = self.labelValue
        else:
            self.createMetada()

    def createMetada(self):
        self.svg  = self.document.getroot()

        # create only dc:description or metadata/RDF/dc:description ?
        metadatas = self.document.xpath('//metadata')
        if metadatas is None or len(metadatas) == 0:
            metadata = Element('metadata')
            metadata.set('id', 'metadatasvg2lvl')
            self.svg.append(metadata)
        else:
            metadata = metadatas[0]

        rdfs = metadata.xpath('//rdf:RDF', NSS)
        if rdfs is None or len(rdfs) == 0:
            rdf = Element(addNS('RDF', 'rdf'))
            metadata.append(rdf)
        else:
            rdf = rdfs[0]

        works = rdf.xpath('//cc:Work', NSS)
        if works is None or len(works) == 0:            
            work = Element(addNS('Work', 'cc'))
            work.set(addNS('about', 'rdf'), '')
            rdf.append(work)
        else:
            work = works[0]

        formats = work.xpath('//dc:format', NSS)
        if formats is None or len(formats) == 0:
            format = Element(addNS('format', 'dc'))
	    format.text = 'image/svg+xml'
            work.append(format)

        types = work.xpath('//dc:type', NSS)
        if types is None or len(types) == 0:
            typeNode = Element(addNS('type', 'dc'))
            typeNode.set(addNS('resource', 'rdf'), 'http://purl.org/dc/dcmitype/StillImage')
            work.append(typeNode)


        description = Element(addNS('description', 'dc'))
	description.text = self.labelValue
        work.append(description)

    def getValue(self, namespace, name=None, dictValues=None, default=None):
        if dictValues is None:
            dictValues = self.label

        try:
            if name is not None:
                value =  dictValues[namespace][name]
            else:
                value = dictValues[namespace]

            if value is None:
                return default
            else:
                return value
        except:
            return default

    def defineWindowHeader(self, title=''):
        self.root = Tkinter.Tk()
        self.root.title(title)
        self.frame = Tkinter.Frame(self.root)
        self.frame.pack()

    def defineOkCancelButtons(self, top, command):
        ok_button = Tkinter.Button(top,
                                   text="OK",
                                   command=command)
        ok_button.pack(side=Tkinter.RIGHT)

        cancel_button = Tkinter.Button(top,
                                       text="Cancel",
                                       command=top.quit)
        cancel_button.pack(side=Tkinter.RIGHT)

    def defineTitle(self, top, label):
        titleFrame = Tkinter.Frame(top, relief=Tkinter.RAISED, borderwidth=1)
        titleFrame.pack(fill=Tkinter.X)

        labelWidget = Tkinter.Label(titleFrame, text=label)
        labelWidget.pack(fill=Tkinter.BOTH, expand=True)

    def defineLabel(self, top, label, alone=True, grid=None):
        labelWidget = Tkinter.Label(top, text=label)
        if grid is not None:
            labelWidget.grid(column=grid[0], row=grid[1])
        else:
            if alone == True:
                labelWidget.pack(anchor=Tkinter.W)
            else:
                labelWidget.pack(side=Tkinter.LEFT)

        return labelWidget

    def defineMessage(self, top, msg):
        msgWidget = Tkinter.Message(top, text=msg)
        msgWidget.pack(fill=Tkinter.X)

    def defineScale(self, top, value, label, from_, to, resolution, default):
        frame = Tkinter.Frame(top)
        frame.pack(fill=Tkinter.X)

        if label is not None:
            self.defineLabel(frame, label, alone=False)
        var = Tkinter.Scale(frame, from_=from_, to=to,
                            resolution=resolution,
                            orient=Tkinter.HORIZONTAL)
        if value is not None:
            var.set(value)
        else:
            var.set(default)
        var.pack(fill=Tkinter.X)

        return (var, frame)

    def defineListbox(self, top, value, label, items):
        import os
        isMacosx = (os.name == 'mac' or os.name == 'posix')

        frame = Tkinter.Frame(top)
        frame.pack(fill=Tkinter.X)

        if label is not None:
            self.defineLabel(frame, label, alone=False)

        scrollbar = Tkinter.Scrollbar(frame, orient=Tkinter.VERTICAL)
        var = Tkinter.Listbox(frame, selectmode=Tkinter.SINGLE,
                              yscrollcommand=scrollbar.set, height=6)
        scrollbar.config(command=var.yview)
        scrollbar.pack(side=Tkinter.RIGHT, fill=Tkinter.Y)

        for item in items:
            var.insert(Tkinter.END, item)

        if value is not None:
            items = var.get(0, Tkinter.END)
            item  = value

            selection = 0
            for i in xrange(len(items)):
                if items[i] == item:
                    selection = i
                    break
            var.activate(selection)
            # this call make the listbox to be badly displayed under macosx.
            if not isMacosx:
                var.selection_set(selection)
        else:
            var.activate(0)
            if not isMacosx:
                var.selection_set(0)
        var.pack(side=Tkinter.RIGHT, fill=Tkinter.BOTH)

        return var

    def defineEntry(self, top, value, label):
        entryLine = Tkinter.Frame(top)
        entryLine.pack(fill=Tkinter.X)

        if label is not None:
            self.defineLabel(entryLine, label, alone=False)

        var = Tkinter.Entry(entryLine)
        if value is not None:
            var.insert(Tkinter.INSERT, value)
        var.pack(side=Tkinter.RIGHT)

        return (var, entryLine)

    def defineCheckbox(self, top, value, label, default=0):
        var = Tkinter.IntVar()
        if value is not None:
            if value == 'true':
                var.set(1)
            else:
                var.set(0)
        else:
            var.set(default)

        if label is not None:
            button = Tkinter.Checkbutton(top, text=label, variable=var)
        else:
            button = Tkinter.Checkbutton(top, variable=var)
        button.pack(anchor=Tkinter.W)

        return var

    def isBoxChecked(self, box):
        if box.get() == 1:
            return 'true'
        else:
            return 'false'

    def fileSelectHook(self, filename):
        pass

    def fileSelectCallback(self):
        openFile = tkFileDialog.askopenfile(parent=self.frame,
                                            mode='rb',
                                            title='Choose a file')
        if openFile is not None:
            openFile.close()
            self.fileSelectHook(openFile.name)

    def defineFileSelectDialog(self, top, value=None, label=None):
        selectionFrame = Tkinter.Frame(top)
        selectionFrame.pack(fill=Tkinter.X)

        if label is not None:
            self.defineLabel(selectionFrame, label, alone=False)

        button = Tkinter.Button(selectionFrame, text="open", command=self.fileSelectCallback)
        button.pack(side=Tkinter.RIGHT)

        var = Tkinter.Entry(selectionFrame)
        if value is not None:
            var.insert(Tkinter.INSERT, value)
        var.pack(side=Tkinter.RIGHT)

        return var

    def defineBitmap(self, top, value, label, command, grid=None, buttonName=''):
        imageFrame = Tkinter.Frame(top)
        if grid is None:
            imageFrame.pack()
        else:
            imageFrame.grid(column=grid[0], row=grid[1])

        imgFilename = join(getInkscapeExtensionsDir(), "xmoto_bitmap", value)

        image   = Image.open(imgFilename)
        tkImage = ImageTk.PhotoImage(image)

        # have to use a lambda function to pass parameters to the callback function
        buttonImage = Tkinter.Button(imageFrame, image=tkImage,
                                     width=92, height=92,
                                     command=lambda : command(label, buttonName))
        buttonImage.tkImage = tkImage
        buttonImage.pack()

        labelImage = Tkinter.Label(imageFrame, text=label)
        labelImage.pack()

        return imageFrame

    def bitmapSelectionWindowHook(self, imgName, buttonName):
        pass

    def setSelectedBitmap(self, imgName, buttonName):
        self.top.destroy()
        self.bitmapSelectionWindowHook(imgName, buttonName)

    def bitmapSelectionWindow(self, title, bitmaps, callingButton):
        self.top = Tkinter.Toplevel(self.root)
        self.top.title(title)
        scrollbarV = Tkinter.Scrollbar(self.top, orient=Tkinter.VERTICAL)
        scrollbarH = Tkinter.Scrollbar(self.top, orient=Tkinter.HORIZONTAL)
        canvas     = Tkinter.Canvas(self.top,
                                    yscrollcommand=scrollbarV.set,
                                    xscrollcommand=scrollbarH.set,
                                    width=512+32, height=512)
        canvas.grid(row=0, column=0, sticky="news")

        scrollbarV.config(command=canvas.yview)
        scrollbarV.grid(row=0, column=1, sticky=Tkinter.N+Tkinter.S)
        scrollbarH.config(command=canvas.xview)
        scrollbarH.grid(row=1, column=0, sticky=Tkinter.E+Tkinter.W)

        self.top.grid_rowconfigure(0, weight=1)
        self.top.grid_columnconfigure(0, weight=1)

        frame = Tkinter.Frame(canvas)

        counter = 0
        keys = bitmaps.keys()
        keys.sort()
        for name in keys:
            imageFilename = bitmaps[name]

            self.defineBitmap(frame, imageFilename, name,
                              command=self.setSelectedBitmap,
                              grid=(counter % 4, counter / 4),
                              buttonName=callingButton)
            counter += 1

        canvas.create_window(0, 0, window=frame)
        frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
        canvas.yview_moveto(0.0)
        canvas.xview_moveto(0.0)

        self.root.wait_window(self.top)

    def defineRadioButtons(self, top, value, buttons, label=None, command=None):
        frame = Tkinter.Frame(top)
        frame.pack(fill=Tkinter.X)

        logging.info("radio button value=%s" % value)

        if label is not None:
            self.defineLabel(frame, label, alone=False)

        var = Tkinter.StringVar()
        if value is not None:
            var.set(value)
        else:
            # default to the first button
            (text, value) = buttons[0]
            var.set(value)

        for text, value in buttons:
            b = Tkinter.Radiobutton(frame, text=text,
                                    variable=var, value=value,
                                    command=command)
            b.pack(side=Tkinter.LEFT)

        return var
