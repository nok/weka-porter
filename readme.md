
# weka-porter

[![Build Status](https://img.shields.io/travis/nok/weka-porter/master.svg)](https://travis-ci.org/nok/weka-porter)
[![PyPI](https://img.shields.io/pypi/v/weka-porter.svg)](https://pypi.python.org/pypi/weka-porter)
[![PyPI](https://img.shields.io/pypi/pyversions/weka-porter.svg)](https://pypi.python.org/pypi/weka-porter)
[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/nok/weka-porter/master/license.txt)

Transpile trained decision trees from [Weka](http://www.cs.waikato.ac.nz/ml/weka/) to C, Java or JavaScript.<br>It's recommended for limited embedded systems and critical applications where performance matters most.


## Benefit

The benefit of the module is to transpile a decision tree from the compact representation by the [Weka](http://www.cs.waikato.ac.nz/ml/weka/) software to a target programming language:

```
outlook = sunny
|   humidity <= 75: yes (2.0)
|   humidity > 75: no (3.0)
outlook = overcast: yes (4.0)
outlook = rainy
|   windy = TRUE: no (2.0)
|   windy = FALSE: yes (3.0)
```

```java
public static String classify(String outlook, boolean windy, double humidity) {
    if (outlook.equals("sunny")) {
        if (humidity <= 75) {
            return "yes";
        }
        else if (humidity > 75) {
            return "no";
        }
    }
    else if (outlook.equals("overcast")) {
        return "yes";
    }
    else if (outlook.equals("rainy")) {
        if (windy == true) {
            return "no";
        }
        else if (windy == false) {
            return "yes";
        }
    }
    return null;
}
```


## Installation

```bash
pip install weka-porter
```


## Usage

Either you use the porter as [imported module](#module) in your application or you use the [command-line interface](#cli).


### Module

This example shows how you can port a decision tree to Java:

```bash
# Download Weka:
wget https://netcologne.dl.sourceforge.net/project/weka/weka-3-8/3.8.2/weka-3-8-2.zip
unzip weka-3-8-2.zip && cd weka-3-8-2

# Train model and save the result:
java -cp weka.jar weka.classifiers.trees.J48 -t data/weather.numeric.arff -v > j48.txt

# Copy and paste the compact representation from 'j48.txt' to a new file (i.e. 'j48_tree.txt') manually.
```

```python
from weka_porter import Porter

porter = Porter(language='java')
output = porter.port('j48_tree.txt', method_name='classify')
print(output)
```

The ported [tree](examples/basics.py#L9-L31) matches the [original version](examples/j48_tree.txt) of the estimator.


### Command-line interface

This examples shows how you can port a estimator from the command line. The estimator can be ported by using the following command:

```
python -m weka_porter --input <txt_file> [--output <destination_dir>] [--c] [--java] [--js]
python -m weka_porter -i <txt_file> [-o <destination_dir>] [--c] [--java] [--js]
```

The target programming language is changeable on the fly:

```bash
python -m weka_porter -i estimator.txt --c
python -m weka_porter -i estimator.txt --java
python -m weka_porter -i estimator.txt --js
```

Finally the following command will display all options:

```bash
python -m weka_porter --help
python -m weka_porter -h
```


## Development

### Environment

Install the required environment [modules](environment.yml) by executing the script [environment.sh](scripts/environment.sh):

```bash
bash ./scripts/environment.sh
```

```bash
conda env create -n weka-porter -f environment.yml
source activate weka-porter
```

Furthermore [Node.js](https://nodejs.org) (`>=6`), [Java](https://java.com) (`>=1.6`) and [GCC](https://gcc.gnu.org) (`>=4.2`) are required for all tests.


### Testing

Run all [tests](tests) by executing the bash script [test.sh](scripts/test.sh):

```bash
bash ./scripts/test.sh
```

```bash
python -m unittest discover -vp '*Test.py'
```

The tests cover module functions as well as matching predictions of ported trees.


## License

The library is Open Source Software released under the [MIT](license.txt) license.


## Questions?

Don't be shy and feel free to contact me on [Twitter](https://twitter.com/darius_morawiec).