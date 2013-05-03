import unittest
from understate.parser import *

class ParserTest(unittest.TestCase):
    class Renderer:
        def onHeader1(self,text):
            pass
        def onEmpty(self,text):
            pass
        def onLine(self,text):
            pass
        def onEnd(self):
            pass
    
    def test_parse_empty_lines(self):
        class EmptyLineRenderer(ParserTest.Renderer):
            def onEmpty(self,text):
                self.okay = True
        r = EmptyLineRenderer()
        parser = Parser(r)
        buf = "\n\n\n"
        parser.parse(buf)
        self.assertTrue(r.okay)

    def test_parse_header1(self):
        class Header1Renderer(ParserTest.Renderer):
            def onHeader1(self,text):
                self.okay = text == "test"
        r = Header1Renderer()
        parser = Parser(r)
        buf = "test\n====\n"
        parser.parse(buf)
        self.assertTrue(r.okay)

    def test_parse_lines(self):
        class LineRenderer(ParserTest.Renderer):
            def __init__(self): self.lines = 0
            def onLine(self,text): self.lines = self.lines + 1

        r = LineRenderer()
        parser = Parser(r)
        buf = "test\n====\nline1\nline2\nline3\n"
        parser.parse(buf)
        self.assertEqual(r.lines,3)

if __name__ == '__main__':
        unittest.main()
