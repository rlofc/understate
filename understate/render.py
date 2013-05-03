import curses
from pyfiglet import Figlet
from pygments import highlight
from pygments.lexers import TextLexer
from pygments.formatters import NullFormatter
from pygmentsext import UnderstateFormatter

class CursesRenderer:
    def __init__(self):
        self.stdscr = curses.initscr()
        curses.cbreak()
        self.stdscr.refresh()
        curses.start_color()
        self.refreshSize();
        curses.init_pair(1,curses.COLOR_RED,curses.COLOR_BLACK)

    def refreshSize(self):
        (self.height,self.width) = self.stdscr.getmaxyx()
        self.header1Font = Figlet(font='computer',justify='center',width=self.width)
        self.header2Font = Figlet(font='doom',justify='center',width=self.width)
        self.header3Font = Figlet(font='threepoint',justify='center',width=self.width)

    def safeaddstr(self,output,attr):
        try: self.stdscr.addstr(output,attr)
        except curses.error: pass

    def onHeader1(self,text):
        output = self.header1Font.renderText(text)
        self.safeaddstr(output,curses.color_pair(1))
        self.stdscr.refresh()

    def onEmpty(self,text):
        self.safeaddstr(text,curses.color_pair(1))
        self.stdscr.refresh()

    def onLine(self,text):
        self.safeaddstr(text.center(self.width),curses.color_pair(1))
        self.stdscr.refresh()

    def onCode(self,text):
        lines = text.split('\n')
        textw = len(max(lines,key=len))
        xpos = (self.width - textw)/2
        (cy,cx) = self.stdscr.getyx()
        subwin = self.stdscr.subwin(len(lines),textw+2,cy,xpos)
        highlight(text,TextLexer(),UnderstateFormatter(style='monokai'),subwin)
        self.stdscr.move(cy+len(lines)+1,0)

    def onEnd(self):
        c = self.stdscr.getch()
        self.stdscr.clear()
