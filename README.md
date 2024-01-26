<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [Introduction](#introduction)
- [Configuration file](#configuration-file)
- [Usage](#usage)
  - [Usage examples](#usage-examples)
- [Tips](#tips)
- [How do I get started?](#how-do-i-get-started)
  - [Installation](#installation)
    - [Using Pip](#using-pip)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# Introduction

`bt-cheater` is a general-purpose cheatsheet tool powered by python.

The tool provides a way search through snippets of text stored in plain-text files using keywords, and all from the commandline.

The search logic relies on a simple structure for the text: a cheat _header_ and _body_, e.g.

```
# python ternary assignments # ternary # variables
    This is a note on python ternary variable assignments
# bash loops # loops
    This is text on bash loop structures
# civil # war # us
    Dates: Apr 12, 1861 - May 9, 1865
```

As illustrated above, the header is comprised of _Cheat Terms_, which are keywords delimited by octothorpes (#). 

The whitespace padding is optional and improves readability.

# Configuration file

`cheater` can read yaml config files formatted as:

```
search:
  paths:
    - ~/Documents/notes
    - ${HOME}/Documents/more_notes
    - ~/notes
  filters:
    - md
    - txt
```

These are the settings recognized by the tool:

| Key     | Value                                      |
|:--------|:-------------------------------------------|
| paths   | List of cheat file paths to search against |
| filters | List of file extensions to search for      |

If no config file is specified, the tool will attempt to read one from the following locations, in order of precedence:

- /etc/bt-cheater/config.yaml
- ./config.yaml
- ~/.bt-cheater/config.yaml

# Usage

```
Usage: cheater find [OPTIONS] TOPICS...

  Find cheat notes according to keywords

Options:
  --version                     Show the version and exit.
  -e, --explode-topics          Write results to their own cheat files
  -c, --cheatfile TEXT          Manually specify cheat file(s) to search
                                against
  -p, --cheatfile-path TEXT     Manually specify cheat file paths to search
                                against
  -a, --any                     Any search term can occur in the topic header
                                (default is "all")
  -b, --search-body             Search against cheat note content instead of
                                topic headers
  --no-pause                    Do not pause between topic output
  --help                        Show this message and exit.

  Examples:
  bt-cheater find -c ~/Documents/cheats.md foo bar baz
  bt-cheater find -c ~/Documents/cheats.md foo bar baz
  bt-cheater -C my_special_config.yaml find -c ~/Documents/cheats.md foo bar baz

  If no config file is specified, the tool will attempt to read one from the
  following locations, in order of precedence:

  - /etc/bt-cheater/config.yaml 
  - ./config.yaml 
  - ~/.bt-cheater/config.yaml
```

## Usage examples

Given: Your config file is configured to search through '~/Documents/notes' 
for cheat files, that is, your configuration file is ~/.bt-cheater/config.yaml, with contents: <br />
```yaml
search:
  paths:
    - ${HOME}/Documents/notes
  filters:
    - md
    - txt
```

* You want to find topic headers containing the words _foo_ _bar_ and _baz_
    * `bt-cheater find foo bar baz`
* You want to search a specific cheat file, _~/Documents/cheats.md_, for topic headers containing the words _foo_ _bar_ and _baz_
    * `bt-cheater find -c ~/Documents/cheats.md foo bar baz`
* Same as above, but you also want to specify your own configuration file _my_special_config.yaml_
    * `bt-cheater -C my_special_config.yaml find -c ~/Documents/cheats.md foo bar baz`<br />
    **Note:** Because you explicitly specified the cheat file, any cheat paths defined in your config will be skipped

# Tips

As bodies of text may overlap in their keyword designation, specifying multiple terms
can help narrow down search results if you specify a search condition.

As such, the default search logic is _all_, where all search terms must occur in the topic header (logically equivalent to AND).

If you want to broaden your search criteria, use the `-a/--any` flag, instructing `bt-cheater` to consider _any_ search term present in the topic header (logically equivalent to OR).

# How do I get started?

## Installation

### Using Pip

- Form pypi.org `pip install bt-cheater`
- Directly from the repo `pip install git+https://github.com/berttejeda/bert.cheater.git`

Or clone this repo, switch to the project root `cd bert.cheater`, and `pip install -e .`,
then calling `python bertdotcheater/cli.py --help`