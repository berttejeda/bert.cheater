class AsciiColors:
    """
    Terminal colors
    """

    def __init__(self):
        self.ascii_green_start = '[92m'
        self.ascii_green_end = '[92m'
        if not __import__("sys").stdout.isatty():
            for _ in dir():
                if isinstance(_, str) and _[0] != "_":
                    locals()[_] = ""
        else:
            # Set Windows console in VT mode
            if __import__("platform").system() == "Windows":
                kernel32 = __import__("ctypes").windll.kernel32
                kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
                del kernel32        

    @staticmethod
    def colorize(color_string, string='', **kwargs):
        ascii_colors = {
            'bold': '[1m',
            'emerald': '[36m',
            'red': '[91m',
            'green': '[92m',
            'yellow': '[93m',
            'purple': '[95m',
            'reset': '[0m'
        }
        if kwargs.get('codeonly'):
            return ascii_colors[color_string]
        else:
            return ascii_colors[color_string] + string + ascii_colors['reset']

    def emerald(self, string):
        return self.colorize('emerald', string)

    def purple(self, string):
        return self.colorize('purple', string)

    def green(self, string):
        return self.colorize('green', string)

    def red(self, string):
        return self.colorize('red', string)

    def yellow(self, string):
        return self.colorize('yellow', string)