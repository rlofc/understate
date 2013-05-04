import curses

from pygments.formatter import Formatter
from pygments.formatters import Terminal256Formatter

# Reuse Terminal256Formatter color approximation capabilities
# so we can create curses color_pairs
class UnderstateFormatter(Terminal256Formatter):
    def _setup_styles(self):
        index = 16 # leave the first 16 pairs for understate
        for ttype, ndef in self.style:
            attrspec = 0
            fg = 0; bg = 235;
            if ndef['color']:
                fg = self._color_index(ndef['color'])
            if ndef['bgcolor']:
                bg = self._color_index(ndef['bgcolor'])
            curses.init_pair(index,fg,bg)
            if self.usebold and ndef['bold']:
                attrspec = attrspec | curses.A_BOLD
            if self.useunderline and ndef['underline']:
                attrspec = attrspec | curses.A_UNDERLINE

            self.styles[ttype] = curses.color_pair(index) | attrspec
            index = index + 1

    def __init__(self, **options):
        Formatter.__init__(self, **options)

        self.xterm_colors = []
        self.best_match = {}
        self.style_string = {}
        self.styles = {}

        self.usebold = 'nobold' not in options
        self.useunderline = 'nounderline' not in options

        self._build_color_table() # build an RGB-to-256 color conversion table
        self._setup_styles() # convert selected style's colors to term. colors

    def format(self, tokensource, outfile):
        for ttype, value in tokensource:
            while ttype not in self.styles:
                ttype = ttype.parent
            outfile.addstr(value.encode('utf-8'),self.styles[ttype])
