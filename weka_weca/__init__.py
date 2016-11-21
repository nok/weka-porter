

class Node:

    def __init__(self, start, end, depth=0):
        self.start = start
        self.scope = []
        self.end = end
        self.depth = depth

    def __str__(self):
        content = '\n'.join([str(node) for node in self.scope])
        return '\n'.join([self.start, content, self.end])


class Porter:

    def __init__(self):
        self.indent = '    '

    def port(self, path):

        # Load data:
        with open(path, 'r') as file:
            content = file.readlines()

        # Parse data:
        tree = Node('', '')
        for line in content:
            line = line.strip()

            depth = line.count('|   ')
            retrn = line.count(':') == 1
            condition = line[(depth * len(self.indent)):]

            # Get current node:
            node = None
            if depth > 0:
                while depth > 0:
                    if node is None:
                        node = tree.scope[-1]
                    else:
                        node = node.scope[-1]
                    depth = depth - 1
            else:
                node = tree.scope

            new = Node('if (' + condition + ') {', '}')
            if retrn:
                new.scope.append('return somewhat')
                if type(node) is list:
                    node.append(new)
                else:
                    node.scope.append(new)
            else:
                if depth > 0:
                    node.scope.append(new)
                else:
                    if type(node) is list:
                        node.append(new)
                    else:
                        node.scope.append(new)

            # if depth <= prev_depth:
            #     out.append(depth * self.indent + '}')

            # out.append(depth * self.indent + 'if (' + condition + ') {')
            # if retrn:
            #     out.append((depth + 1) * self.indent + 'return somewhat;')
            #     out.append((depth) * self.indent + '}')
            # else:
            #     prev_depth = depth

            # print(condition)
            # print(booom)


            #
            # indents = line.count('|   ') * self.indent
            # print()
            # print('original:')
            # print(line)
            # print('output:')
            # condition = line[len(indents):]

        return str(tree)
