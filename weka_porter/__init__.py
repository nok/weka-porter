

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
        """
        Print the current node with all sub nodes.

        Return
        ------
        :return : string
            The ported scope of the node.
        """
        indent = self.depth * self.indent
        nl = '\n'
        scope = nl.join([str(node) for node in self.scope])
        result = nl.join([indent + self.start, scope, indent + self.end])
        return result


class Porter:
    """Main class to port a decision tree from the Weka format."""

    __version__ = '0.1.0'

    # @formatter:off
    TEMPLATES = {
        'c': {
            'method': {
                'open':     '{return_type} {method_name}({atts}) {{',
                'close':    '}'
            },
            'if':           'if ({cond}) {{',
            'elif':         'else if ({cond}) {{',
            'data': {
                'string':   'string',
                'int':      'int',
                'bool':     'bool',
                'double':   'double',
            },
            'indent':       '    ',
        },
        'java': {
            'method': {
                'open':     'public static {return_type} {method_name}({atts}) {{',
                'close':    '    return null;\n }'
            },
            'if':           'if ({cond}) {{',
            'elif':         'else if ({cond}) {{',
            'data': {
                'string':   'String',
                'int':      'int',
                'bool':     'boolean',
                'double':   'double',
            },
            'indent':       '    ',
        },
        'js': {
            'method': {
                'open':     'var {method_name} = function({atts}) {{',
                'close':    '}'
            },
            'if':           'if ({cond}) {{',
            'elif':         'else if ({cond}) {{',
            'data': {
                'string':   '',
                'int':      '',
                'bool':     '',
                'double':   '',
            },
            'indent':       '    ',
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

    def temp(self, name, templates=None):
        """
        Get the specific template of the chosen programming language.

        Parameters
        ----------
        :param name : string
            The key name of the template.
        :param tempaltes : string
            The template with placeholders.

        Returns
        -------
        :return : string
            The required template string.
        """
        if templates is None:
            templates = self.TEMPLATES.get(self.language)
        keys = name.split('.')
        key = keys.pop(0).lower()
        template = templates.get(key, None)
        if type(template) is str:
            return template
        else:
            keys = '.'.join(keys)
            return self.temp(keys, templates=template)

    def port(self, path, method_name='classify'):
        """
        Convert a single decision tree as a function.

        Parameters
        ----------
        :param path : string
            The path of the exported text file.
        :param method_name : string (default='classify')
            The method name.

        Return
        ------
        :return : string
            The ported tree.
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
                        return_type = self.temp('data.int')
                    elif return_type in ['TRUE', 'FALSE']:
                        return_type = self.temp('data.bool')
                    else:
                        return_type = self.temp('data.string')

            att_name = cond.split(' ')[0]
            att_type = self.temp('data.string')
            if any(x in cond for x in ['TRUE', 'FALSE']):
                att_type = self.temp('data.bool')
                cond = cond.replace('TRUE', 'true')
                cond = cond.replace('FALSE', 'false')
            elif any(x in cond for x in ['>', '>=', '<', '<=']):
                att_type = self.temp('data.double')
            else:
                parts = cond.split(' ')
                parts.append('"%s"' % parts.pop())
                cond = ' '.join(parts)

            if ' = ' in cond:
                if self.language == 'java' and att_type.lower() == 'string':
                    cond = cond.replace(' = ', '.equals(') + ')'
                else:
                    cond = cond.replace(' = ', ' == ')

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
        method_open = self.temp('method.open').format(
            return_type=return_type, method_name=method_name, atts=atts)
        method_close = self.temp('method.close')

        result = ''.join([method_open, str(root), method_close])
        return result
