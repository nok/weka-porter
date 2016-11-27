import os
import argparse

from . import Porter


def main():
    parser = argparse.ArgumentParser(
        description=('Transpile a decision tree from Weka '
                     'to a low-level programming language.'),
        epilog='More details on: https://github.com/nok/weka-tree-porter')
    parser.add_argument(
        '--input', '-i',
        required=True,
        help='Set the path of an exported tree in Weka format.')
    parser.add_argument(
        '--output', '-o',
        required=False,
        help='Set the destination directory.')
    parser.add_argument(
        '--language', '-l',
        choices=['c', 'java', 'js'],
        default='java',
        required=False,
        help='Set the target programming language.')
    parser.add_argument(
        '--print', '-p',
        required=False,
        default=False,
        help='Set whether the result should be printed to the console.')

    args = vars(parser.parse_args())
    arg_input = str(args['input'])
    arg_output = str(args['output'])
    arg_print = args['print']
    arg_language = args['language']

    if arg_input.endswith('.txt') and os.path.isfile(arg_input):
        porter = Porter(language=arg_language)
        result = porter.port(arg_input)

        if arg_print is True:
            print(result)
        else:
            filename = 'result.txt'
            path = arg_input.split(os.sep)
            del path[-1]
            path += [filename]
            path = os.sep.join(path)
            if arg_output != '' and os.path.isdir(arg_output):
                path = os.path.join(arg_output, filename)
            with open(path, 'w') as file:
                file.write(result)

if __name__ == "__main__":
    main()
