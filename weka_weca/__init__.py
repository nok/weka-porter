
class Porter:

    def __init__(self):
        self.indent = '    '

    def port(self, path):
        # Result:
        out = []

        # Load data:
        with open(path, 'r') as file:
            content = file.readlines()

        # Remove whitespace:
        for line in content:
            line = line.strip()
            # action!

        return ''.join(out)
