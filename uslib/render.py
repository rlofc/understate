import curses
from pyfiglet import Figlet
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import NullFormatter
from pygmentsext import UnderstateFormatter
from random import shuffle
from datetime import datetime
from time import sleep

class CursesRenderer:
    def __init__(self):
        self.stdscr = curses.initscr()
        curses.cbreak()
        self.stdscr.refresh()
        curses.start_color()
        self.refreshSize();
        curses.init_pair(1,curses.COLOR_WHITE,curses.COLOR_BLACK)
        curses.init_pair(2,curses.COLOR_RED,curses.COLOR_BLACK)
        curses.init_pair(3,curses.COLOR_YELLOW,curses.COLOR_BLACK)
        self.currentSlide = 0
        self.lastHeader = ''
        self.screenmtx = []
        for y in range(self.height-1):
            for x in range(self.width):
                self.screenmtx.append([y,x])
        shuffle(self.screenmtx)
        self.currentLineLength = 0
        self.padForLine = None
    def clean(self):
        curses.endwin()

    def refreshSize(self):
        (self.height,self.width) = self.stdscr.getmaxyx()
        self.header1Font = Figlet(font='computer',justify='center',width=self.width)
        self.header2Font = Figlet(font='doom',justify='center',width=self.width)
        self.header3Font = Figlet(font='threepoint',justify='center',width=self.width)

    def safeaddstr(self,output,attr):
        try: self.stdscr.addstr(output,attr)
        except curses.error: pass

    def fade(self):
        curses.curs_set(0)
        tpc = float(1/float(len(self.screenmtx)))
        for t in self.screenmtx:
            m1 = datetime.now()
            self.stdscr.addch(t[0],t[1],' ')
            self.stdscr.refresh()
            m2 = datetime.now()
            if (m2-m1).microseconds/1000000.0 < tpc:
                sleep(tpc - ((m2-m1).microseconds/1000000.0))
        curses.curs_set(1)

    def newSlide(self):
        if self.currentSlide > 0:
            c = self.stdscr.getch()
            self.fade()
            self.stdscr.clear()
        self.currentSlide = self.currentSlide + 1

    def willNotOverflow(self,nLines,textw):
        (cy,cx) = self.stdscr.getyx()
        return (nLines+cy) < self.height - 2 and textw < self.width - 2

    def unIndent(self,text):
        diff = len(text)-len(text.lstrip())
        if (diff>0):
            text = text[diff:]
            text = text.replace('\n'+(' ' * diff),'\n')
        return text

    def onHeader(self,groups,font):
        text = groups["text"]
        output = font.renderText(text)
        self.safeaddstr(output,curses.color_pair(3))
        self.stdscr.refresh()
        self.lastHeader = text

    def onHeader1(self,groups):
        self.newSlide()
        self.onHeader(groups,self.header1Font)

    def onHeader2(self,groups):
        self.newSlide()
        self.onHeader(groups,self.header2Font)

    def onHeader3(self,groups):
        self.newSlide()
        self.onHeader(groups,self.header3Font)

    def onEmpty(self,groups):
        self.safeaddstr('\n',curses.color_pair(1))
        self.stdscr.refresh()

    def closeLine(self):
        if self.padForLine:
            (cy,cx) = self.stdscr.getyx()
            if cy<self.height-1:
                self.padForLine.refresh(0,0,cy,(self.width-self.currentLineLength)/2,cy,(self.width-self.currentLineLength)/2+self.currentLineLength)
                self.currentLineLength = 0
                self.stdscr.move(cy+1,0)
            else:
                self.currentLineLength = 0

    def appendToLine(self,text):
        if self.currentLineLength == 0:
            (cy,cx) = self.stdscr.getyx()
            self.padForLine = curses.newpad(1,self.width)
        self.padForLine.addstr(text,curses.color_pair(0))
        self.currentLineLength = self.currentLineLength+len(text)
        if self.currentLineLength>(self.width-(self.width/4)):
            self.closeLine()

    def onLine(self,groups):
        text = groups["text"]
        self.appendToLine(text)

    def onLink(self,groups):
        text = groups["link"]
        self.appendToLine(text)

    def onLineFeed(self,groups):
        self.closeLine()

    def onImage(self,groups):
        pass

    def onCode(self,groups):
        text = groups["text"]
        text = self.unIndent(text)
        syntax = "text"
        if groups.has_key("syntax"):
            syntax = groups["syntax"]
            if syntax=='':syntax = 'text'
        lines = text.split('\n')
        nLines = len(lines)
        textw = len(max(lines,key=len))

        if self.willNotOverflow(nLines,textw):
            xpos = (self.width - textw)/2
            (cy,cx) = self.stdscr.getyx()
            padMargins = curses.newpad(nLines+1,textw+2)
            padMargins.bkgd(' ',curses.color_pair(16))
            padMargins.refresh(0,0,cy+1,xpos-1,cy+2+nLines,xpos+textw+2)
            padCode = curses.newpad(nLines,textw+1)
            padCode.bkgd(' ',curses.color_pair(16))
            highlight(text,get_lexer_by_name(syntax),UnderstateFormatter(style='monokai'),padCode)
            padCode.refresh(0,0,cy+2,xpos,cy+1+nLines,xpos+textw+1)
            self.stdscr.move(cy+nLines+2,0)

    def onList(self,groups):
        text = groups["text"]
        lines = text.split('\n')
        nLines = len(lines)
        textw = len(max(lines,key=len))

        if self.willNotOverflow(nLines,textw):
            xpos = (self.width - textw)/2
            (cy,cx) = self.stdscr.getyx()
            padList = curses.newpad(nLines,textw+2)
            padList.addstr(text,curses.color_pair(2))
            padList.refresh(0,0,cy+1,xpos,cy+1+nLines,xpos+textw+2)
            self.stdscr.move(cy+nLines,1)

    def onEnd(self):
        self.newSlide()
