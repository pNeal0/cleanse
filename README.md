# Cleanse

## What is this?
This script is used for clearing up filenames in your directories so that they don't contain special characters and whitespaces

## Prerequisites
*Python3

## How to use it
```
$ python cleanse.py --help
usage: cleanse [-h] [-d] [-r] [-v] [-n] [-i] [-l] [-c [CHARACTER]] [-t FILETYPE]
               [-w WHITELIST]
               [DIRECTORY]

wipe filenames of special characters

positional arguments:
  DIRECTORY

options:
  -h, --help            show this help message and exit
  -d, --dotfiles        Ignore dotfiles
  -r, --recursive       Run recursively
  -v, --verbose         Output information about changes made
  -n, --dry-run         Preview changes without modifying
  -i, --interactive     Prompt for confirmation before modifying files
  -l, --lowercase       Lowercase filenames
  -c [CHARACTER], --character [CHARACTER]
                        Use CHARACTER instead of blanks
  -t FILETYPE, --filetype FILETYPE
                        Only operate on files of this type
  -w WHITELIST, --whitelist WHITELIST
                        Ignore these files (comma separated list)

```

## Example
![screen-gif](./example_usage.gif)
