import curses
from pyfiglet import Figlet
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import NullFormatter
from pygmentsext import UnderstateFormatter

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

    def newSlide(self):
        if self.currentSlide > 0:
            c = self.stdscr.getch()
            self.stdscr.clear()
        self.currentSlide = self.currentSlide + 1

    def willNotOverflow(self,nLines):
        (cy,cx) = self.stdscr.getyx()
        return (nLines+cy) < self.height - 2

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

    def onLine(self,groups):
        text = groups["text"]
        self.safeaddstr(text.center(self.width),curses.color_pair(0))
        self.stdscr.refresh()

    def onCode(self,groups):
        text = groups["text"]
        text = self.unIndent(text)
        syntax = "text"
        if groups.has_key("syntax"):
            syntax = groups["syntax"]
            if syntax=='':syntax = 'text'
        lines = text.split('\n')
        nLines = len(lines)

        if self.willNotOverflow(nLines):
            textw = len(max(lines,key=len))
            xpos = (self.width - textw)/2
            (cy,cx) = self.stdscr.getyx()

            margins = self.stdscr.subwin(nLines+1,textw+2,cy+1,xpos-1)
            margins.bkgd(' ',curses.color_pair(16))
            subwin = self.stdscr.subwin(nLines,textw+1,cy+2,xpos)
            subwin.bkgd(' ',curses.color_pair(16))
            highlight(text,get_lexer_by_name(syntax),UnderstateFormatter(style='monokai'),subwin)
            self.stdscr.move(cy+nLines+2,0)

    def onList(self,groups):
        text = groups["text"]
        lines = text.split('\n')
        nLines = len(lines)
    
        if self.willNotOverflow(nLines):
            textw = len(max(lines,key=len))
            xpos = (self.width - textw)/2
            (cy,cx) = self.stdscr.getyx()

            subwin = self.stdscr.subwin(nLines,textw+2,cy+1,xpos)
            subwin.addstr(text,curses.color_pair(2))
            self.stdscr.move(cy+nLines,1)

    def onEnd(self):
        self.newSlide()
