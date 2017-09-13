# -*- coding: utf-8 -*-

import os
import sys
import argparse

from . import Porter


def parse_args(args):
    parser = argparse.ArgumentParser(
        description=('Transpile a decision tree from Weka '
                     'to a low-level programming language.'),
        epilog='More details on: https://github.com/nok/weka-porter')
    parser.add_argument(
        '--input', '-i',
        required=True,
        help='Set the path of an exported tree in Weka format.')
    parser.add_argument(
        '--output', '-o',
        required=False,
        help='Set the destination directory.')
    languages = {
        'c': 'C',
        'java': 'Java',
        'js': 'JavaScript'
    }
    parser.add_argument(
        '--language', '-l',
        choices=languages.keys(),
        default='java',
        required=False,
        help=argparse.SUPPRESS)
    for key, lang in list(languages.items()):
        parser.add_argument(
            '--{}'.format(key),
            action='store_true',
            help='Set {} as the target programming language.'.format(lang))
    parser.add_argument(
        '--print', '-p',
        required=False,
        default=False,
        help='Set whether the result should be printed to the console.')
    args = vars(parser.parse_args(args))
    return args


def main():
    args = parse_args(sys.argv[1:])

    arg_input = str(args['input'])
    arg_output = str(args['output'])
    arg_print = args['print']

    # Check input data:
    if not arg_input.endswith('.txt') or not os.path.isfile(arg_input):
        error = 'No valid txt file found.'
        sys.exit('Error: {}'.format(error))

    # Determine language:
    arg_language = str(args['language'])
    languages = ['c', 'java', 'js']
    for key in languages:
        if args.get(key):  # found explicit assignment
            arg_language = key
            break

    try:
        porter = Porter(language=arg_language)
        output = porter.port(arg_input)
    except Exception as e:
        sys.exit('Error: {}'.format(str(e)))
    else:
        if arg_print is True:
            print(output)
        else:
            filename = 'result.txt'
            path = arg_input.split(os.sep)
            del path[-1]
            path += [filename]
            path = os.sep.join(path)
            if arg_output != '' and os.path.isdir(arg_output):
                path = os.path.join(arg_output, filename)
            with open(path, 'w') as file_:
                file_.write(output)


if __name__ == "__main__":
    main()
