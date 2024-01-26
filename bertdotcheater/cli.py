#!/usr/bin/env python
# coding=utf-8
""" Utility for searching through cheat sheets
"""
# Imports
from __future__ import print_function
from bertdotcheater.ascii import AsciiColors
from bertdotcheater.logger import Logger
from bertdotcheater.processor import CheatFileProcessor
from getversion import get_module_version
import bertdotcheater
import glob
import logging
import os
import sys
import time
from pyaml_env import parse_config
import click

# Private variables
__author__ = 'etejeda'
__version__ = get_module_version(bertdotcheater)[0]
__required_sections = [
    'paths'
]

# Globals
debug = False
verbose = 0
log_file = None
loglevel = None
logger = None

config_file = 'config.yaml'
config_path = None
colors = AsciiColors()

# Initialize logging facility
logger = Logger().init_logger(__name__)

def load_config():
    """ Load config file
    """
    global debug, config_file, config_path
    config_path_strings = [
        os.path.realpath(os.path.expanduser(os.path.join('~', '.bt-cheater'))),
        '.', '/etc/bt-cheater'
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
                cfg = type('obj', (object,), parse_config(config_path))
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
    e.g. config.yaml:
    search:
      paths:
        - ~/cheats
        - C:\\Users\\tomtester\\Documents\\notes
      filters:
        - md
        - txt
If no config file is specified, the tool will attempt to read one from the following locations, in order of precedence:

- /etc/bt-cheater/config.yaml
- ~/.bt-cheater/config.yaml
- ./config.yaml
    """
    global config_file
    # Overriding globals
    configfile_p = kwargs.get('config')
    if configfile_p:
        config_file = os.path.realpath(os.path.expanduser(kwargs['config']))
    if not os.path.exists(config_file) and configfile_p:
        logger.warning("Couln't find %s" % colors.yellow(config_file))
    debug = kwargs['debug']
    verbose = kwargs['verbose']
    if debug:
        loglevel = logging.DEBUG  # 10
    elif verbose:
        loglevel = logging.INFO  # 20
    else:
        loglevel = logging.INFO  # 20
    # Set logging format
    # Set up a specific logger with our desired output level
    logger.setLevel(loglevel)
    return 0

epilog = """\b
Examples:
bt-cheater find -c ~/Documents/cheats.md foo bar baz
bt-cheater find -c ~/Documents/cheats.md foo bar baz
bt-cheater -C my_special_config.yaml find -c ~/Documents/cheats.md foo bar baz

If no config file is specified, the tool will attempt to 
read one from the following locations, in order of precedence:

- /etc/bt-cheater/config.yaml

- ~/.bt-cheater/config.yaml

- ./config.yaml
"""
@cli.command('find',
             short_help='Retrieve cheat notes from specified cheatfiles according to keywords',
             epilog=epilog)
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
        logger.error('No valid config file found!')
        logger.info(epilog)
        sys.exit(1)
    filetypes = config.search['filters'] if config.search.get('filters') else ['md', 'txt']
    logger.debug('Searching against file types %s' % ','.join(filetypes))
    explode = True if kwargs['explode_topics'] else False
    if kwargs.get('cheatfile'):
        explicit_cheatfiles = []
        if sys.version_info[0] == 2:
            for cf in kwargs['cheatfile']:
                explicit_cheatfiles += glob.glob(os.path.expanduser(cf))
        if sys.version_info[0] >= 3:
            for cf in kwargs['cheatfile']:
                explicit_cheatfiles += glob.glob(os.path.expanduser(cf), recursive=True)
    else:
        explicit_cheatfiles = []
    cheatfile_paths = kwargs.get('cheatfile_path')
    if cheatfile_paths:
        cheatfile_paths = [os.path.expanduser(p) for p in cheatfile_paths] + config.search['paths']
    else:
        cheatfile_paths = [os.path.expanduser(p) for p in config.search['paths']]
    logger.debug(f"Cheat file paths set to {','.join(cheatfile_paths)}")

    # Execution time
    start_time = time.time()
    # If any specified cheatfile paths are directories, walk through and append to cheatfile list
    cheatfiles = gather_cheatfiles(cfpaths=cheatfile_paths, cftypes=filetypes)
    cf_processor = CheatFileProcessor(**kwargs)

    if explicit_cheatfiles:
        for cheatfile in explicit_cheatfiles:
            if cheatfile:
                cf_processor.process_cheat_file(cheatfile)
    else:
        for cheatfile in cheatfiles:
            if cheatfile:
                cf_processor.process_cheat_file(cheatfile)
    end_time = time.time()
    action = "Wrote" if explode else "Retrieved"
    logger.info(
        f'{action} {len(cf_processor.matched_topics)} topic(s) in {(end_time - start_time):.2f} seconds'
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
    else:
      logger.warning('Could not find any cheat files!')
      yield ()

if __name__ == '__main__':
    sys.exit(cli(sys.argv[1:]))
