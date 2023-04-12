#! /usr/bin/env python3

import argparse
import os
import re
import sys

preset = {}


def get_args():
    parser = argparse.ArgumentParser(
        description='Generate an .env file from a template',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Preset: Values read from an existing .env file

Template Rule:
  1. Not in key = value format (mostly comments)
    template
  2. key =
    preset or user input
  3. key = ? command
    preset or command output or user input
  4. key = ! command
    preset or command output
  5. key = * [default]
    preset or default or user input or empty
  6. key = value
    value
''')
    parser.add_argument('-c', '--clear', action='store_true', default=False,
                        help='Not loading .env file')
    parser.add_argument('-t', '--template', type=str, default='./env',
                        help='Template file path')
    parser.add_argument('-o', '--output-dir', type=str, default='.',
                        help='Output directory path')
    return parser.parse_args()


def load_env(fname):
    try:
        with open(fname, 'rt') as f:
            tmp = {}
            for line in f.readlines():
                line = re.sub(r'#.*', '', line).strip()
                if not line:
                    continue
                key, val = map(str.strip, line.split('='))
                tmp[key] = val.strip("'")
            return tmp
    except FileNotFoundError:
        pass
    return {}


def prompt(key, val='', required=True):
    try:
        while True:
            tip = '' if val or required else '(Enter - Skip)'
            res = input(f'{key} [{val}]{tip} ').strip()
            if res:
                return res
            if val or not required:
                return val
    except (EOFError, KeyboardInterrupt):
        print()
        sys.exit()


def process(line):
    def shell(cmd):
        return os.popen(cmd).read().strip()

    tmp = re.sub(r'#.*', '', line).strip()
    if tmp.find('=') == -1:
        line = line.strip()
        print(line)
        return line

    key, val = map(str.strip, tmp.split('='))

    if not val:
        val = preset.get(key, '')
        val = prompt(key, val)
    elif val[0] == '?':
        val = preset.get(key) or shell(val[1:])
        val = prompt(key, val)
    elif val[0] == '!':
        val = preset.get(key) or shell(val[1:])
    elif val[0] == '*':
        val = preset.get(key) or val[1:].strip().strip("'")
        val = prompt(key, val, False)
    else:
        val = val.strip("'")

    if len(val.split()) > 1:
        val = f"'{val}'"

    return f'{key}={val}'


def main():
    global preset

    args = get_args()
    env_path = os.path.join(args.output_dir, '.env')

    if not args.clear:
        preset = load_env(env_path)

    output = []
    with open(args.template, 'rt') as f:
        output = [process(line) for line in f.readlines()]

    with open(env_path, 'wt') as f:
        f.write('\n'.join(output))
        f.write('\n')


if __name__ == '__main__':
    main()
