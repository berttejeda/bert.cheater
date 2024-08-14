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

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# Introduction

This is a Golang rewrite of the python equivalent [bert.cheater.python](https://github.com/berttejeda/bert.cheater.python).

The tool provides a way search through snippets of text stored in plain-text files using keywords, and all from the command-line.

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

`bert.cheater` can read yaml config files formatted as:

```yaml
search:
  paths: # Where to search for notes
    - ~/Documents/workspace/tmp
    - ~/Documents/workspace/tmp2
    - ~/Documents/workspace/tmp3
  filters: # Files to filter against
    - md
    - txt
any: false # Match any vs all topics, not yet implemented
nopause: false # If true, don't pause between matched topics
```

If no config file is specified, the tool will attempt to read one from the following locations, in order of precedence:

- /etc/bert.cheater/config.yaml
- ./config.yaml
- ~/.bert.cheater/config.yaml

# Usage

`bert.cheater --help`:

```
usage: bert.cheater [<flags>] <command> [<args> ...]

Search through your markdown notes by keyword


Flags:
      --[no-]help          Show context-sensitive help (also try --help-long and --help-man).
  -v, --[no-]verbose       Enable verbose mode
  -d, --[no-]debug         Enable debug mode
  -J, --[no-]json-logging  Enable json log format
  -c, --config=CONFIG      Override Config File to use
      --[no-]version       Show application version.

Commands:
help [<command>...]
    Show help.

find [<flags>] [<args>...]
    Retrieve cheat notes and display in terminal
```

`bert.cheater find --help`:

```
usage: bert.cheater find [<flags>] [<args>...]

Retrieve cheat notes and display in terminal


Flags:
      --[no-]help          Show context-sensitive help (also try --help-long and --help-man).
  -v, --[no-]verbose       Enable verbose mode
  -d, --[no-]debug         Enable debug mode
  -J, --[no-]json-logging  Enable json log format
  -c, --config=CONFIG      Override Config File to use
      --[no-]version       Show application version.
  -a, --[no-]any           Match 'any' topic as opposed to 'all'
  -n, --[no-]no-pause      Don't pause between matched topics
  -f, --filters=md... ...  File extensions to math when searching
  -p, --paths=. ...        File search paths

Args:
  [<args>]  Topics to match
```

## Usage examples

For your convenience, see the [examples](examples) directory.

# Tips

As bodies of text may overlap in their keyword designation, specifying multiple terms
can help narrow down search results if you specify a search condition.

As such, the default search logic is _all_, where all search terms must occur in the topic header (logically equivalent to AND).

Not Yet Implemented: If you want to broaden your search criteria, use the `-a/--any` flag, instructing `bert.cheater` to consider _any_ search term present in the topic header (logically equivalent to OR).

# How do I get started?

## Installation

* Install via `go install`<br />
`go install github.com/berttejeda/bert.cheater@latest`
* Download a [release](https://github.com/berttejeda/bert.cheater/releases)
