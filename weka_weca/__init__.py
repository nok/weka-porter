

class Node:
    """Data structure of a single node."""

    def __init__(self, start, end, depth=0, indent='    '):
        """
        Wrap string initially around string.

        Parameters
        ----------
        :param start : string
            The start of the if-condition.
        :param end : string
            The end of the if-condition.
        :param depth : integer
            The indentation depth.
        :param indent : string
            The indentation style.
        """
        self.start = start
        self.scope = []
        self.end = end
        self.depth = depth
        self.indent = indent

    def __str__(self):
        indent = self.depth * self.indent
        scope  = '\n'.join([str(node) for node in self.scope])
        result = '\n'.join([indent + self.start, scope, indent + self.end])
        return result


def port(path, method_name='classify'):
    """
    Convert a single decision tree as a function.

    Parameters
    ----------
    :param path : string
        The path of the exported text file.
    :param method_name : string (default='classify')
        The method name.
    :return:
    """

    # Load data:
    with open(path, 'r') as file:
        content = file.readlines()

    # Create root node:
    root = Node('', '')
    atts = []

    # Construct tree:
    for line in content:
        line = line.strip()
        depth = line.count('|   ')

        # Get current node:
        node = None
        d = depth
        if d > 0:
            while d > 0:
                node = root.scope[-1] if node is None else node.scope[-1]
                d -= 1
        else:
            node = root.scope

        # Get always the scope list:
        if type(node) is not list:
            node = node.scope

        # Build the condition:
        cond = line[(depth * len('|   ')):]
        has_return = line.count(':') == 1
        if has_return:
            cond = cond.split(':')[0]
        atts.append(cond.split(' ')[0])
        cond = Node('if (%s) {' % cond, '}', depth=depth+1)

        # Set condition logic:
        if has_return:
            indent = cond.indent * (depth + 2)
            return_value = line[line.find(':') + 1 : line.find('(')].strip()
            return_value = indent + 'return %s;' % str(return_value)
            cond.scope.append(return_value)
        node.append(cond)

    # Merge the relevant attributes:
    atts = list(set(atts))
    atts.sort()
    atts = ', '.join(['float ' + a for a in atts])

    # Wrap function scope around built tree:
    result = ''.join(['int %s function(%s) {'%
                      (method_name, atts), str(root), '}'])

    return result
