#!/usr/bin/env python

import argparse
import core


parser = argparse.ArgumentParser()
parser.add_argument('--state', '-s')
arguments = parser.parse_args()


def main():
    core.users(arguments.state)


if __name__ == '__main__':
    main()
