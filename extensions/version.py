import logging, log
from listAvailableElements import functions2versions, params2versions

class Version:
    def __init__(self):
        # old version... (0.1.1)
        self.x = 0
        self.y = 1
        self.z = 1

    def getXmotoRequiredVersion(self, options, rootLayer):
        # http://wiki.xmoto.tuxfamily.org/index.php?title=Others_tips_to_make_levels
        self.options = options
        if self.options.has_key('sky'):
            self.addVersion((0, 2, 5))
        if self.options['level']['tex'] != '':
            self.addVersion((0, 2, 5))
        if self.options['level'].has_key('music') and self.options['level']['music'] not in [None, '', 'None']:
            self.addVersion((0, 2, 5))
        if self.options.has_key('remplacement'):
            for key, value in self.options['remplacement'].iteritems():
                if value not in ['None', '', None]:
                    self.addVersion((0, 2, 5))
                    break
        if self.options.has_key('layer'):
            self.addVersion((0, 2, 7))
        
        if self.options['level']['lua'] not in [None, '']:
            self.addVersion((0,1,10))
            self.analyseScript(self.options['level']['lua'])

        self.analyseLevelElements(rootLayer)

        return (self.x, self.y, self.z)

    def analyseScript(self, scriptFilename):
        import re

        # every word can be a function, we test them all
        function  = re.compile(r'[a-zA-Z0-9]+')
        functions = {}

        f = open(scriptFilename)
        lines = f.readlines()
        f.close

        for line in lines:
            length = len(line)
            offset    = 0
            while True:
                m = function.search(line, offset)
                if m == None:
                    break
                if m:
                    if m.end() >= length:
                        break
                    # we use a dic instead of a set because sets are
                    # available only since python 2.4 (we need 2.3 compatibility for macosx)
                    functions[line[m.start():m.end()]] = ""
                    offset = m.end()

        for function in functions.iterkeys():
            if functions2versions.has_key(function):
                version = functions2Versions[function]
                self.addVersion(version)

    def analyseLevelElements(self, layer):
        for child in layer.children:
            self.analyseLevelElements(child)

        for element in layer.elements:
            for namespace, params in element.elementInformations.iteritems():
                if type(params) == dict:
                    for paramKey in params.iterkeys():
                        if (namespace, paramKey) in params2versions:
                            self.addVersion(params2versions[(namespace, paramKey)])

    def addVersion(self, version):
        x,y,z = version
        if x > self.x:
            self.x = x
            self.y = y
            self.z = z
        elif x == self.x:
            if y > self.y:
                self.y = y
                self.z = z
            elif y == self.y:
                if z > self.z:
                    self.z = z

