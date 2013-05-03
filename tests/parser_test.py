import unittest
from understate.parser import *

class ParserTest(unittest.TestCase):
    class Renderer:
        def onHeader1(self,groups):
            pass
        def onHeader2(self,groups):
            pass
        def onHeader3(self,groups):
            pass
        def onEmpty(self,groups):
            pass
        def onLine(self,groups):
            pass
        def onCode(self,groups):
            pass
        def onList(self,groups):
            pass
        def onEnd(self):
            pass
    
    def test_parse_empty_lines(self):
        class EmptyLineRenderer(ParserTest.Renderer):
            def onEmpty(self,groups):
                self.okay = True
        r = EmptyLineRenderer()
        parser = Parser(r)
        buf = "\n\n\n"
        parser.parse(buf)
        self.assertTrue(r.okay)

    def test_parse_header1(self):
        class Header1Renderer(ParserTest.Renderer):
            def onHeader1(self,groups):
                self.okay = groups["text"] == "test"
        r = Header1Renderer()
        parser = Parser(r)
        buf = "test\n====\n"
        parser.parse(buf)
        self.assertTrue(r.okay)

    def test_parse_header1_variant(self):
        class Header1Renderer(ParserTest.Renderer):
            def onHeader1(self,groups):
                self.okay = groups["text"] == "test"
        r = Header1Renderer()
        parser = Parser(r)
        buf = "#test\n"
        parser.parse(buf)
        self.assertTrue(r.okay)

    def test_parse_header2(self):
        class Header1Renderer(ParserTest.Renderer):
            def onHeader2(self,groups):
                self.okay = groups["text"] == "test"
        r = Header1Renderer()
        parser = Parser(r)
        buf = "test\n----\n"
        parser.parse(buf)
        self.assertTrue(r.okay)

    def test_parse_header2_variant(self):
        class Header1Renderer(ParserTest.Renderer):
            def onHeader2(self,groups):
                self.okay = groups["text"] == "test"
        r = Header1Renderer()
        parser = Parser(r)
        buf = "##test\n"
        parser.parse(buf)
        self.assertTrue(r.okay)

    def test_parse_headerr(self):
        class Header1Renderer(ParserTest.Renderer):
            def onHeader3(self,groups):
                self.okay = groups["text"] == "test"
        r = Header1Renderer()
        parser = Parser(r)
        buf = "###test\n"
        parser.parse(buf)
        self.assertTrue(r.okay)

    def test_parse_lines(self):
        class LineRenderer(ParserTest.Renderer):
            def __init__(self): self.lines = 0
            def onLine(self,groups): self.lines = self.lines + 1

        r = LineRenderer()
        parser = Parser(r)
        buf = "test\n====\nline1\nline2\nline3\n"
        parser.parse(buf)
        self.assertEqual(r.lines,3)

    def test_parse_code(self):
        class CodeRenderer(ParserTest.Renderer):
            def onCode(self,groups):
                self.okay = groups["text"] == "int a = 1;"
        r = CodeRenderer()
        parser = Parser(r)
        buf = "```c\nint a = 1;```"
        parser.parse(buf)
        self.assertTrue(r.okay)

    def test_parse_list(self):
        class CodeRenderer(ParserTest.Renderer):
            def onList(self,groups):
                ret = "* item1\n* item2\n"
                self.okay = groups["text"] == ret

        r = CodeRenderer()
        parser = Parser(r)
        buf = "* item1\n* item2\n"
        parser.parse(buf)
        self.assertTrue(r.okay)

if __name__ == '__main__':
        unittest.main()
