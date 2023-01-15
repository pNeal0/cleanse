#!/usr/bin/env python

import os
import sys
import re
import argparse

parser = argparse.ArgumentParser(prog = "cleanse",
                                 description = "wipe filenames of special characters")

parser.add_argument("DIRECTORY",
                    nargs="?",
                    default=os.getcwd())

parser.add_argument("-d", "--dotfiles",
                    help="Ignore dotfiles",
                    action="store_true")

parser.add_argument("-r", "--recursive",
                    help="Run recursively",
                    action="store_true")

parser.add_argument("-v", "--verbose",
                    help="Output information about changes made",
                    action="store_true")

parser.add_argument("-n", "--dry-run",
                    help="Preview changes without modifying",
                    action="store_true")

parser.add_argument("-i", "--interactive",
                    help="Prompt for confirmation before modifying files",
                    action="store_true")

parser.add_argument("-l", "--lowercase",
                    help="Lowercase filenames",
                    action="store_true")

parser.add_argument("-c", "--character",
                    help="Use CHARACTER instead of blanks",
                    nargs="?",
                    const="",
                    default="")

parser.add_argument("-t", "--filetype",
                    help="Only operate on files of this type",
                    default=None)

parser.add_argument("-w", "--whitelist",
                    help="Ignore these files (comma separated list)",
                    default=None)

args = parser.parse_args()


def contains_special_chars(filename):
    if not re.search(f"^[a-zA-Z0-9\.\-\_]*$", filename):
        return True
    else:
        return False


def remove_special_chars(filename, character):
    return re.sub("[^a-zA-Z0-9\.\-\_]", character, filename)


def get_files(directory):
    # get list of all files in directory
    file_list = os.listdir(directory)
    # clean up the file list
    file_list_clean = []
    for file in file_list:

        # skip if whitelisted
        if args.whitelist and file in args.whitelist.split(","):
            continue

        # skip if begins with a dot
        if args.dotfiles and re.search("^\.", file):
            continue

        # skip if doesnt end with specified extension
        if args.filetype and not file.endswith(args.filetype):
            continue

        file_list_clean.append(file)

    return file_list_clean


def main(directory):
    for filename in get_files(directory):
        file_path = os.path.join(directory, filename)

        # traverse subdirectories
        if args.recursive and os.path.isdir(file_path):
            main(file_path)

        # skip file if no persmission to write
        if not os.access(file_path, os.W_OK):
            sys.stderr.write(f"skipping {file_path}, no write permission\n")
            continue

        # check if filename contains special characters
        if contains_special_chars(filename):
            # create a new filename, substituting special characters with args.character
            filename_new = remove_special_chars(filename, args.character)
            # lowercase the filename
            if args.lowercase:
                filename_new = filename_new.lower()


            # only print the change, do not rename the filename
            if args.dry_run:
                print(f"{file_path} -> {os.path.join(directory, filename_new)}")

            else:
                # prompt before renaming the filename if --interactive flag is set
                if args.interactive:
                    print(f"Rename {file_path} to {os.path.join(directory, filename_new)}?")
                    print("y/n ", end="")
                    while True:
                        answer = input()
                        if answer == "y" or answer == "Y":
                            # rename the file
                            os.rename(os.path.join(directory, filename),
                                      os.path.join(directory, filename_new))
                            break
                        elif answer == "n" or answer == "N":
                            break
                        else:
                            continue
                else:
                    # rename the file
                    os.rename(os.path.join(directory, filename),
                              os.path.join(directory, filename_new))
                    # print the change
                    if args.verbose:
                        print(f"{file_path} -> {os.path.join(directory, filename_new)}")


# exit early if directory doesn't exist
if not os.path.isdir(args.DIRECTORY):
    sys.stderr.write(f"directory {args.DIRECTORY} doesn't exist\n")
    exit(1)

main(args.DIRECTORY)
