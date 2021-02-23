#!/usr/bin/env python
# coding=utf-8
""" Utility for searching through cheat sheets
"""
# Imports
from __future__ import print_function
import glob
import io
import itertools
import logging
import logging.handlers
import os
import re
import sys
import time

# OS Detection
is_windows = True if sys.platform in ['win32', 'cygwin'] else False
is_darwin = True if sys.platform in ['darwin'] else False

# Account for script packaged as an exe via cx_freeze
if getattr(sys, 'frozen', False):
    # frozen
    self_file_name = script_name = os.path.basename(sys.executable)
    project_root = os.path.dirname(os.path.abspath(sys.executable))
else:
    # unfrozen
    self_file_name = os.path.basename(__file__)
    if self_file_name == '__main__.py':
        script_name = os.path.dirname(__file__)
    else:
        script_name = self_file_name
    project_root = os.path.dirname(os.path.abspath(__file__))

# Modify our sys path to include the script's location
sys.path.insert(0, project_root)
# Make the zipapp work for python2/python3
py_path = 'py3' if sys.version_info[0] >= 3 else 'py2'
sys.path.insert(0, os.path.join(project_root, 'libs', py_path))

# Import third-party modules
try:
    import click
    import yaml
except ImportError as e:
    print('Error in %s ' % os.path.basename(self_file_name))
    print('Failed to import at least one required module')
    print('Error was %s' % e)
    print('Please install/update the required modules:')
    print('pip install -U -r requirements.txt')
    sys.exit(1)

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

# Private variables
__author__ = 'etejeda'
__version__ = 'v1.1.9'
__required_sections = [
    'paths'
]
__auth__ = 'cheater.auth'

# Globals
debug = False
verbose = 0
log_file = None
loglevel = None
logger = None

config_file = 'cheater.yaml'
config_path = None
colors = AsciiColors()


def load_config():
    """ Load config file
    """
    global debug, config_file, config_path
    config_path_strings = [
        os.path.realpath(os.path.expanduser(os.path.join('~', '.cheater'))),
        '.', '/etc/cheater'
    ]
    config_paths = [os.path.join(p, config_file) for p in config_path_strings]
    config_found = False
    config_is_valid = False
    for config_path in config_paths:
        config_exists = os.path.exists(config_path)
        config_is_valid = False
        if config_exists:
            config_found = True
            try:
                with open(config_path, 'r') as ymlfile:
                    cfg = type('obj', (object,), yaml.load(ymlfile))
                config_is_valid = all([cfg.search.get(section) for section in __required_sections])
                logger.info("Found config file - {cf}".format(cf=colors.emerald(config_path)))
                if not config_is_valid:
                    logger.warning(
                        """At least one required section is not defined in your config file: {cf}.""".format(
                            cf=colors.yellow(config_path))
                    )
                    logger.warning("Review the available documentation or consult --help")
                config_file = config_path
                break
            except Exception as e:
                logger.warning(
                    "I encountered a problem reading your config file: {cp}, error was {err}".format(
                        cp=config_path, err=colors.red(str(e)))
                )
    if config_found and config_is_valid:
        return cfg
    else:
        return None

@click.group()
@click.version_option(version=__version__)
@click.option('--config', '-C', type=str, nargs=1, help='Specify a config file (default is config.ini)')
@click.option('--debug', '-d', is_flag=True, help='Enable debug output')
@click.option('--verbose', '-v', count=True, help='Increase verbosity of output')
@click.option('--log', '-l', type=str, help='Specify (an) optional log file(s)')
def cli(**kwargs):
    """
\b
Work with cheat files
\b
Settings can be defined in config file (--config/-C)
    e.g. cheater.yaml:
    search:
      paths:
        - ~/cheats
        - C:\\Users\\tomtester\\Documents\\notes
      filters:
        - md
        - txt
If no config file is specified, the tool will attempt to read one from the following locations, in order of precedence:
- /etc/cheater.yaml
- ./cheater.yaml
- ~/.cheater/cheater.yaml
    """
    global config_file, debug, verbose, loglevel, logger
    # Overriding globals
    configfile_p = kwargs.get('config')
    if configfile_p:
        config_file = os.path.realpath(os.path.expanduser(kwargs['config']))
    debug = kwargs['debug']
    logfilename = kwargs['log']
    verbose = kwargs['verbose']
    if debug:
        loglevel = logging.DEBUG  # 10
    elif verbose:
        loglevel = logging.INFO  # 20
    else:
        loglevel = logging.INFO  # 20
    # Set logging format
    # Set up a specific logger with our desired output level
    logger = logging.getLogger('logger')
    logger.setLevel(loglevel)
    if logfilename:
        # Add the log  file handler to the logger
        filehandler = logging.handlers.RotatingFileHandler(logfilename, maxBytes=10000000, backupCount=5)
        formatter = logging.Formatter(
            "[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
        filehandler.setFormatter(formatter)
        logger.addHandler(filehandler)
    streamhandler = logging.StreamHandler()
    streamhandler.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s"))
    logger.addHandler(streamhandler)
    logger.debug('Debug Mode Enabled')
    if not os.path.exists(config_file) and configfile_p:
        logger.warning("Couln't find %s" % colors.yellow(config_file))
    return 0


@cli.command('find',
             short_help='Retrieve cheat notes from specified cheatfiles according to keywords',
             epilog="""\b
Examples:
cheater find -c ~/Documents/cheats.md foo bar baz
cheater find -c ~/Documents/cheats.md foo bar baz
cheater -C my_special_config.yaml find -c ~/Documents/cheats.md foo bar baz

If no config file is specified, the tool will attempt to read one from the following locations, in order of precedence:

- /etc/cheater.yaml
- ./cheater.yaml
- ~/.cheater/cheater.yaml
""")
@click.version_option(version=__version__)
@click.option('--explode-topics', '-e',
              is_flag=True,
              help='Write results to their own cheat files')
@click.option('--cheatfile', '-c',
              type=str, nargs=1,
              help='Manually specify cheat file(s) to search against',
              multiple=True)
@click.option('--cheatfile-path', '-p',
              type=str, nargs=1,
              help='Manually specify cheat file paths to search against',
              multiple=True)
@click.option('--local_cheat_cache', '-L',
              default='~/.cheater',
              help='Specify root folder you want to store cheats as retrieved from git (defaults to ~/.cheater)')
@click.option('--force_git_updates', '-F',
              is_flag=True,
              help='Force updates for cheat repos retrieved via git')
@click.option('--any', '-a',
              is_flag=True,
              help='Any search term can occur in the topic header (default is "all")')
@click.option('--search-body', '-b',
              is_flag=True,
              help='Search against cheat note content instead of topic headers')
@click.option('--no-pause', is_flag=True, help='Do not pause between topic output')
@click.argument('topics',
                required=True,
                nargs=-1)
def find_cheats(**kwargs):
    """ Find cheat notes according to keywords
    """
    # Load config defaults
    config = load_config()
    if config is None:
        logger.error('No valid config file found. Consult README.md')
        sys.exit(1)
    filetypes = config.search['filters'] if config.search.get('filters') else ['md', 'txt']
    # Parse parameters
    search_topics = kwargs['topics']
    condition = 'any' if kwargs['any'] else 'all'
    search_body = True if kwargs['search_body'] else False
    no_pause = kwargs.get('no_pause')
    if no_pause:
        pause = False
    else:
        pause = True
    explode = True if kwargs['explode_topics'] else False
    if kwargs.get('cheatfile'):
        cheatfiles = []
        if sys.version_info[0] == 2:
            for cf in kwargs['cheatfile']:
                cheatfiles += glob.glob(os.path.expanduser(cf))
        if sys.version_info[0] >= 3:
            for cf in kwargs['cheatfile']:
                cheatfiles += glob.glob(os.path.expanduser(cf), recursive=True)
    else:
        cheatfiles = []
    cheatfile_paths = kwargs['cheatfile_path']
    if cheatfile_paths:
        cheatfile_paths = [p for p in cheatfile_paths] + config.search['paths']
    else:
        cheatfile_paths = config.search['paths']
    # Build regular expression
    search_list = []
    if condition == 'all':
        regx = '.*%s'
        # Account for ALL permutations of the list of search topics
        search_permutations = list(itertools.permutations(list(search_topics)))
        for sp in search_permutations:
            search_list.append('(%s)|' % ''.join([regx % p for p in sp]))
        search = ''.join(search_list)
    else:
        regx = '.*%s|'
        search = ''.join([regx % t for t in search_topics])
    search = re.sub('\|$', '', search)
    logger.debug('Regular expression is: %s' % search)
    # Compile the regular expression
    string = re.compile(search)
    # Initialize defaults
    matched_topics = []
    # Warn if search body is enabled
    if search_body:
        logger.warning('Search includes cheat body; can\'t yet reliably determine count of matched topics')
    # Execution time
    start_time = time.time()
    # If any specified cheatfile paths are directories, walk through and append to cheatfile list
    for cheatfile in gather_cheatfiles(cfpaths=cheatfile_paths, cftypes=filetypes):
        if os.path.exists(cheatfile) and not os.path.isdir(cheatfile):
            try:
                with io.open(cheatfile, "r", encoding="utf-8") as n:
                    cheats = n.readlines()
            except UnicodeDecodeError:
                try:
                    with io.open(cheatfile, "r") as n:
                        cheats = n.readlines()
                except Exception:
                    print()
            cheats_length = len(cheats)
            topics = [(i, n) for i, n in enumerate(cheats) if n.startswith('# ')]
            # else:
            #     topics_count = len([s for s in topics if s[1].startswith('# ') and string.search(s[1])])
            #     print('Found %s topic(s) matching your search' % topics_count)
            for index, line in enumerate(topics):
                # Find the corresponding line index
                s_line_index = topics[index][0]
                # Skip topics not matching search term (if applicable)
                cheat_topic = cheats[s_line_index]
                match_length = len(string.search(cheat_topic).group()) if string.search(cheat_topic) else []
                if not any([match_length, search_body]):
                    continue
                if not search_body:
                    logger.info(
                        'Topic search criteria matched against cheat file: {cf}'.format(
                            cf=colors.emerald(cheatfile)))
                # Find the next corresponding line index
                s_next_line_index = cheats_length if index + 1 > len(topics) - 1 else topics[index + 1][0]
                # Grab the topic headers
                header_list = ['# %s' % header.strip() for header in cheat_topic.split('# ') if header]
                headers = ' '.join(sorted(set(header_list), key=header_list.index))
                # headers = '# %s' % ' # '.join([h for h in headers])
                # Get the topic's body
                body = ''.join([l for l in cheats[s_line_index + 1:s_next_line_index] if l])
                body_matched_strings = string.search(body) if search_body else None
                if not any([string.search(cheat_topic), body_matched_strings]):
                    continue
                try:
                    if search_body:
                        body = body_matched_strings.group().encode('utf-8')
                except Exception:
                    logger.error('Failed to search body for this topic: {c}'.format(
                        c=colors.red(cheat_topic)))
                # utf-8 encoding
                try:
                    headers = str(headers.encode('utf-8').decode('utf8'))
                    body = str(body.encode('utf-8').decode('utf8'))
                except UnicodeEncodeError:
                    try:
                        body = str(body.encode('utf-8'))
                    except Exception:
                        logger.error('I had trouble encoding this topic: {c}'.format(
                            c=colors.red(cheat_topic)))
                        continue
                if explode:
                    output_filename = re.sub("\s|#|:|/|'", "_", headers.split('#')[1].strip()) + '.md'
                    try:
                        with io.open(output_filename, "a", encoding="utf-8") as text_file:
                            print("{h}\n{b}".format(h=colors.purple(headers), b=colors.green(body)))
                            text_file.write("{h}\n{b}".format(h=headers, b=body))
                            matched_topics.append(headers)
                        if pause:
                            wait = input("PRESS ENTER TO CONTINUE TO NEXT TOPIC or 'q' to quit ")
                            if wait.lower() == 'q':
                                sys.exit()
                    except Exception:
                        logger.error('Failed to write {h} ... skipping'.format(h=headers))
                else:
                    try:
                        print('{h}\n{b}'.format(h=colors.purple(headers), b=colors.green(body)))
                        matched_topics.append(headers)
                        if pause:
                            wait = input("ENTER => CONTINUE TO NEXT TOPIC or 'q' to quit ")
                            if wait.lower() == 'q':
                                sys.exit()                            
                    except Exception:
                        logger.error('Failed to process topic ... skipping')
                        continue
    end_time = time.time()
    action = "Wrote" if explode else "Retrieved"
    logger.info('%s %s topic(s) in %0.2f seconds' % (
        action, len(matched_topics), (end_time - start_time))
                )

def gather_cheatfiles(**kwargs):
    cheatfile_paths = kwargs.get('cfpaths')
    filetypes = kwargs.get('cftypes')
    if any([os.path.isdir(cfo) for cfo in cheatfile_paths]):
        for cfp in cheatfile_paths:
            if os.path.isdir(cfp):
                logger.info('Processing cheat files under %s' % colors.purple(cfp))
                for root, directories, files in os.walk(cfp):
                    directories[:] = [d for d in directories if not d.startswith('.')]
                    for filename in files:
                        if any([filename.endswith(ft) for ft in filetypes]):
                            filepath = os.path.join(root, filename)
                            yield filepath

if __name__ == '__main__':
    sys.exit(cli(sys.argv[1:]))
