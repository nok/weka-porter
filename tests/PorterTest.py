import subprocess as subp
import unittest

from weka_porter import Porter


class PorterTest(unittest.TestCase):

    def setUp(self):
        self.porter = Porter(language='java')
        subp.call(['mkdir', '.tmp'])  # $ mkdir .temp

    def tearDown(self):
        subp.call(['rm', '-rf', '.tmp'])  # $ rm -rf .temp
        del self.porter

    def test_classification_1(self):
        """Test string, boolean and double variables as features."""

        temp = ("class {class_name} {{"
                "\n    {method}"
                "\n    public static void main(String[] args) {{"
                "\n        String result = {class_name}.{method_name}(args[0], Boolean.valueOf(args[1]), Double.valueOf(args[2]));"
                "\n        System.out.println(result);"
                "\n    }}"
                "\n}}")

        class_name = 'Test'
        method_name = 'classify'

        model = self.porter.port('./examples/weather_data.txt', method_name=method_name)

        path = './.tmp/%s.java' % class_name
        with open(path, 'w') as f:
            content = temp.format(
                class_name=class_name,
                method_name=method_name,
                method=model)
            f.write(content)
        # $ javac ./.tmp/Test.java
        subp.call(['javac', path])

        # $ java -classpath temp <temp_filename> <features>
        cmd = ['java', '-classpath', '.tmp', class_name]
        args = ['sunny', 'true', '80']
        cmd += args
        pred = subp.check_output(cmd, stderr=subp.STDOUT).strip()
        self.assertEqual(str(pred), 'no')

    def test_classification_2(self):
        """Test string, boolean and double variables as features."""

        temp = ("class {class_name} {{"
                "\n    {method}"
                "\n    public static void main(String[] args) {{"
                "\n        String result = {class_name}.{method_name}(args[0], Boolean.valueOf(args[1]), Double.valueOf(args[2]));"
                "\n        System.out.println(result);"
                "\n    }}"
                "\n}}")

        class_name = 'Test'
        method_name = 'classify'

        model = self.porter.port('./examples/weather_data.txt',
                                 method_name=method_name)

        path = './.tmp/%s.java' % class_name
        with open(path, 'w') as f:
            content = temp.format(
                class_name=class_name,
                method_name=method_name,
                method=model)
            f.write(content)
        # $ javac ./.tmp/Test.java
        subp.call(['javac', path])

        # $ java -classpath temp <temp_filename> <features>
        cmd = ['java', '-classpath', '.tmp', class_name]
        args = ['rainy', 'false', '80']
        cmd += args
        pred = subp.check_output(cmd, stderr=subp.STDOUT).strip()
        self.assertEqual(str(pred), 'yes')

    def test_classification_3(self):
        """Test string, boolean and double variables as features."""

        temp = ("class {class_name} {{"
                "\n    {method}"
                "\n    public static void main(String[] args) {{"
                "\n        int result = {class_name}.{method_name}(args[0], Boolean.valueOf(args[1]), Double.valueOf(args[2]));"
                "\n        System.out.println(result);"
                "\n    }}"
                "\n}}")

        class_name = 'Test'
        method_name = 'classify'

        model = self.porter.port('./examples/weather_num_data.txt', method_name=method_name)

        path = './.tmp/%s.java' % class_name
        with open(path, 'w') as f:
            content = temp.format(
                class_name=class_name,
                method_name=method_name,
                method=model)
            f.write(content)
        # $ javac ./.tmp/Test.java
        subp.call(['javac', path])

        # $ java -classpath temp <temp_filename> <features>
        cmd = ['java', '-classpath', '.tmp', class_name]
        args = ['sunny', 'true', '80']
        cmd += args
        pred = subp.check_output(cmd, stderr=subp.STDOUT).strip()
        self.assertEqual(str(pred), '-1')

    def test_classification_4(self):
        """Test string, boolean and double variables as features."""

        temp = ("class {class_name} {{"
                "\n    {method}"
                "\n    public static void main(String[] args) {{"
                "\n        int result = {class_name}.{method_name}(args[0], Boolean.valueOf(args[1]), Double.valueOf(args[2]));"
                "\n        System.out.println(result);"
                "\n    }}"
                "\n}}")

        class_name = 'Test'
        method_name = 'classify'

        model = self.porter.port('./examples/weather_num_data.txt',
                                 method_name=method_name)

        path = './.tmp/%s.java' % class_name
        with open(path, 'w') as f:
            content = temp.format(
                class_name=class_name,
                method_name=method_name,
                method=model)
            f.write(content)
        # $ javac ./.tmp/Test.java
        subp.call(['javac', path])

        # $ java -classpath temp <temp_filename> <features>
        cmd = ['java', '-classpath', '.tmp', class_name]
        args = ['rainy', 'false', '80']
        cmd += args
        pred = subp.check_output(cmd, stderr=subp.STDOUT).strip()
        self.assertEqual(str(pred), '1')
