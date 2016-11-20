import os
import argparse

from . import Porter


def main():
    parser = argparse.ArgumentParser(
        description=('Transpile trained scikit-learn models '
                     'to a low-level programming language.'),
        epilog='More details on: https://github.com/nok/sklearn-porter')
    parser.add_argument(
        '--input', '-i',
        required=True,
        help='Set the path of an exported model in pickle (.pkl) format.')
    parser.add_argument(
        '--output', '-o',
        required=False,
        help='Set the destination path.')
    parser.add_argument(
        '--print', '-p',
        required=False,
        default=False,
        help='Set the destination path.')

    args = vars(parser.parse_args())
    arg_input = str(args['input'])
    arg_output = str(args['output'])
    arg_print = args['print']

    if arg_input.endswith('.txt') and os.path.isfile(arg_input):
        porter = Porter()
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
