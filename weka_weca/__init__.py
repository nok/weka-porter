

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
        nl = '\n'
        scope = nl.join([str(node) for node in self.scope])
        result = nl.join([indent + self.start, scope, indent + self.end])
        return result


class Porter:

    # @formatter:off
    TEMPLATES = {
        'c': {
            'method':   '{return_type} {method_name}({atts}) {{',
            'if':       'if ({cond}) {{',
            'elif':     'else if ({cond}) {{',
            'indent':   '    ',
        },
        'java': {
            'method': 'public static {return_type} {method_name}({atts}) {{',
            'if':       'if ({cond}) {{',
            'elif':     'else if ({cond}) {{',
            'indent':   '    ',
        },
        'js': {
            'method': 'var {method_name} = function({atts}) {{',
            'if':       'if ({cond}) {{',
            'elif':     'else if ({cond}) {{',
            'indent':   '    ',
        }
    }
    # @formatter:on

    def __init__(self, language='java'):
        """
        Parameters
        ----------
        :param language : string
            The target programming language.
        """
        self.language = language

    def temp(self, key):
        try:
            return self.TEMPLATES.get(self.language).get(key)
        except IndexError:
            raise IndexError('Template with key \' %s \' not found.' % key)

    def port(self, path, method_name='classify'):
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
        with open(path, 'r') as _file:
            content = _file.readlines()

        # Create root node:
        root = Node('', '')
        return_type = None
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

            # Get always the list:
            if type(node) is not list:
                node = node.scope

            # Build the condition:
            cond = line[(depth * len('|   ')):].strip()
            has_return = ':' in cond
            if has_return:
                parts = cond.split(':')
                cond = parts[0].strip()
                if return_type is None:
                    return_type = parts[1].strip().split(' ')[0]
                    if return_type.isdigit():
                        return_type = 'int'
                    elif return_type in ['TRUE', 'FALSE']:
                        return_type = 'bool'
                    else:
                        return_type = 'String' \
                            if self.language in ['java', 'js'] else 'string'

            if ' = ' in cond:
                cond = cond.replace(' = ', ' == ')

            att_name = cond.split(' ')[0]
            att_type = 'String' if self.language in ['java', 'js'] else 'string'
            if any(x in cond for x in ['TRUE', 'FALSE']):
                att_type = 'bool'
                cond = cond.replace('TRUE', 'true')
                cond = cond.replace('FALSE', 'false')
            elif any(x in cond for x in ['>', '>=', '<', '<=']):
                att_type = 'float'
            else:
                parts = cond.split(' ')
                parts.append('"%s"' % parts.pop())
                cond = ' '.join(parts)

            atts.append('%s %s' % (att_type, att_name))

            if_temp = 'if' if len(node) == 0 else 'elif'
            if_temp = self.temp(if_temp).format(cond=cond)
            cond = Node(if_temp, '}', depth=depth + 1)

            # Set condition logic:
            if has_return:
                indent = cond.indent * (depth + 2)
                return_value = line[line.find(':') + 1: line.find('(')].strip()
                if return_type.lower() == 'string':
                    return_value = '"%s"' % return_value
                return_value = indent + 'return %s;' % str(return_value)
                cond.scope.append(return_value)
            node.append(cond)

        # Merge the relevant attributes:
        atts = list(set(atts))
        atts.sort()
        atts = ', '.join(atts)

        # Wrap function scope around built tree:

        method = self.temp('method').format(
            return_type=return_type, method_name=method_name, atts=atts)
        result = ''.join([method, str(root), '}'])

        return result
