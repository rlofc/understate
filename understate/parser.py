import re
class Parser:

    # Some class constants
    M_REGEX    = 0 # index of regex in matchers tuples
    M_RENDERER = 1 # index of renderer method in matchers tuples

    # Markdown regular expressions
    RE_H1       = r"(?P<text>.*)\n[=]=*\n"
    RE_EMPTY    = r"\n"
    RE_LINE     = r"(?P<text>.*)\n"

    def __init__(self,renderer):
        self.matchers = [
            ( Parser.RE_H1, renderer.onHeader1 ),
            ( Parser.RE_EMPTY, renderer.onEmpty ),
            ( Parser.RE_LINE, renderer.onLine )
        ]

    def _match(self,regex,buf):
        e = re.match(regex,buf,re.MULTILINE)
        text = None
        if e:
            if e.groups() == ():
                text = buf[e.start():e.end()]
            else:
                text = e.group('text')
            buf = buf[e.end():]
        return (e!=None,buf,text)
   
    def parse(self,buf):
        while (len(buf)>0):
            for r in self.matchers:
                (res,buf,text) = self._match(r[Parser.M_REGEX],buf)
                if res:
                    output = r[Parser.M_RENDERER](text)
                    break
