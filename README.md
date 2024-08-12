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

This is a Golang rewrite of [bert.cheater](https://github.com/berttejeda/bert.cheater), a general-purpose, command-line notes tool written in python.

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

`bt-cheater` can read yaml config files formatted as:

```
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

These are the settings recognized by the tool:

| Key     | Value                        |
|:--------|:-----------------------------|
| paths   | Where to search for notes    |
| filters | Files to filter against      |
| pause.  | Pause between matched topics |

If no config file is specified, the tool will attempt to read one from the following locations, in order of precedence:

- /etc/bt-cheater/config.yaml
- ./config.yaml
- ~/.bt-cheater/config.yaml

# Usage

`bt-cheater --help`:

```
usage: bt-cheater [<flags>] <command> [<args> ...]

Search through your markdown notes by keyword


Flags:
      --[no-]help          Show context-sensitive help (also try --help-long and --help-man).
  -v, --[no-]verbose       Enable verbose mode
  -d, --[no-]debug         Enable debug mode
  -J, --[no-]json-logging  Enable json log format

Commands:
help [<command>...]
    Show help.

find [<flags>] [<args>...]
    Retrieve cheat notes and display in terminal
```

`bt-cheater find --help`:

```
usage: bt-cheater find [<flags>] [<args>...]

Retrieve cheat notes and display in terminal


Flags:
      --[no-]help          Show context-sensitive help (also try --help-long and --help-man).
  -v, --[no-]verbose       Enable verbose mode
  -d, --[no-]debug         Enable debug mode
  -J, --[no-]json-logging  Enable json log format
  -a, --[no-]any           Match 'any' topic as opposed to 'all'
  -n, --[no-]no-pause      Don't pause between matched topics
  -f, --filters=md... ...  File extensions to math when searching
  -p, --paths=. ...        File search paths

Args:
  [<args>]  Topics to match
```

## Usage examples

Given: Your config file is configured to search through '~/Documents/notes' 
for cheat files, that is, your configuration file is ~/.bt-cheater/config.yaml, with contents: <br />
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
nopause: true # Don't pause between matched topics
```

* You want to find topic headers containing the words _foo_ _bar_ and _baz_
    * `bt-cheater find foo bar baz`

# Tips

As bodies of text may overlap in their keyword designation, specifying multiple terms
can help narrow down search results if you specify a search condition.

As such, the default search logic is _all_, where all search terms must occur in the topic header (logically equivalent to AND).

If you want to broaden your search criteria, use the `-a/--any` flag, instructing `bt-cheater` to consider _any_ search term present in the topic header (logically equivalent to OR).

# How do I get started?

## Installation

* Install via `go install`<br />
`go install github.com/berttejeda/bert.cheater.go@latest`
