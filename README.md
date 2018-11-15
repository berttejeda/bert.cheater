# Introduction

`cheater` is a general-purpose cheatsheet tool powered by python.

The tool provides a way search through snippets of text stored in plain-text files.

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
    - C:\Users\myusername\Documents\workspace\md
    - ~/Documents
    - ~/cheats
  filters:
    - md
    - txt
```

as with:

```
search:
  paths:
    - C:\Users\tomtester\Documents\cheats
  filters:
    - md
    - txt
```

These are the settings recognized by the tool:

||Key||Value||
|paths|List of cheat file paths to search against|
|filters|List of file extensions to search for|

If no config file is specified, the tool will attempt to read one from the following locations, in order of precedence:

- /etc/cheater.yaml
- ./cheater.yaml
- ~/cheater.yaml


# Usage

```
Usage: cheater.py find [OPTIONS] TOPICS...

  Find cheat notes according to keywords

Options:
  --version                     Show the version and exit.
  -e, --explode-topics          Write results to their own cheat files
  -c, --cheatfile TEXT          Manually specify cheat file(s) to search
                                against
  -p, --cheatfile-path TEXT     Manually specify cheat file paths to search
                                against
  -L, --local_cheat_cache TEXT  Specify root folder you want to store cheats
                                as retrieved from git (defaults to ~/.cheater)
  -F, --force_git_updates       Force updates for cheat repos retrieved via
                                git
  -a, --any                     Any search term can occur in the topic header
                                (default is "all")
  -b, --search-body             Search against cheat note content instead of
                                topic headers
  --help                        Show this message and exit.

  Examples:
  cheater find -c ~/Documents/cheats.md foo bar baz
  cheater find -c ~/Documents/cheats.md foo bar baz
  cheater -C my_special_config.yaml find -c ~/Documents/cheats.md foo bar baz
```

## Usage examples

* For cheat file _~/Documents/cheats.md_, you want to find topic headers containing the words _foo_ _bar_ and _baz_
    * `cheater find -c ~/Documents/cheats.md foo bar baz`
* For cheat file _~/Documents/cheats.md_, you want to find topic headers containing the words _foo_ _bar_ and _baz_, 
additionally, you want to specify your own configuration file _my_special_config.ini_
    * `cheater -C my_special_config.ini find -c ~/Documents/cheats.md foo bar baz`

# Tips

As bodies of text may overlap in their keyword designation, specifying multiple terms
can help narrow down search results if you specify a search condition.

As such, the default search logic is _all_, where all search terms must occur in the topic header (logically equivalent to AND).

If you want to broaden your search criteria, use the `-a/--any` flag, instructing `cheater` _any_ search term to be present in the topic header (logically equivalent to OR).

# How do I get started?

## Installation

    * Using `pip`
        ```pip install git+https://github.com/berttejeda/bert.cheater.git```
    * Downloading a release (It's just a zip-application with self-contained dependencies)
    * Cloning this repo and running `pip install -r requirements`, then working with `cheater.py`