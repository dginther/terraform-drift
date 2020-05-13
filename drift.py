#!/usr/bin/env python

import argparse
import core
import pprint
from colorama import Fore, Back, Style, init

init(autoreset=True)

parser = argparse.ArgumentParser()
parser.add_argument('--state', '-s')
parser.add_argument('--modules', '-m', action='append')
arguments = parser.parse_args()


def main():
    for module in arguments.modules:
        if module == "users":
            print(Fore.GREEN + "============== IAM USERS =============\n\n")
            core.users(arguments.state)
            print(Fore.GREEN + "======================================\n\n")

        if module == "groups":
            print(Fore.GREEN + "============== IAM GROUPS =============\n\n")
            core.groups(arguments.state)
            core.group_policy_attachments(arguments.state)
            print(Fore.GREEN + "======================================\n\n")


if __name__ == '__main__':
    main()
