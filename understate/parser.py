import re
class Parser:

    RE_H1 = r"(?P<text>.*\n)[=]=*\n"
    RE_EMPTY = r"\n"
    RE_LINE = r".*\n"

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
            text = buf[e.start():e.end()]
            buf = buf[e.end():]
        return (e!=None,buf,text)
   
    def parse(self,buf):
        while (len(buf)>0):
            for r in self.matchers:
                (res,buf,text) = self._match(r[0],buf)
                if res:
                    output = r[1](text)
                    break
