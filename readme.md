
# weka-porter

[![Build Status](https://img.shields.io/travis/nok/weka-porter/master.svg)](https://travis-ci.org/nok/weka-porter)
[![PyPI](https://img.shields.io/pypi/v/weka-porter.svg)](https://pypi.python.org/pypi/weka-porter)
[![PyPI](https://img.shields.io/pypi/pyversions/weka-porter.svg)](https://pypi.python.org/pypi/weka-porter)
[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/nok/weka-porter/master/license.txt)

Port or transpile trained decision trees from [Weka](http://www.cs.waikato.ac.nz/ml/weka/) to a low-level programming language like [C](https://en.wikipedia.org/wiki/C_(programming_language)), [Java](https://en.wikipedia.org/wiki/Java_(programming_language)) or [JavaScript](https://en.wikipedia.org/wiki/JavaScript).<br>It's recommended for limited embedded systems and critical applications where performance matters most.


## Benefit

The benefit of the module is to transpile a decision tree from the compact representation by the [Weka](http://www.cs.waikato.ac.nz/ml/weka/) software to a target programming language.

### Input

```
outlook = sunny
|   humidity <= 75: yes (2.0)
|   humidity > 75: no (3.0)
outlook = overcast: yes (4.0)
outlook = rainy
|   windy = TRUE: no (2.0)
|   windy = FALSE: yes (3.0)
```

### Output

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

```sh
pip install weka-porter
```


## Usage

Either you use the porter as [imported module](#module) in your application or you use the [command-line interface](#cli).


### Module

This example shows how you can port a decision tree to Java:

```python
from weka_porter import Porter

porter = Porter(language='java')
result = porter.port('weather_data.txt', method_name='classify')
print(result)
```

The ported [tree](examples/basics.py#L9-L31) matches the [original version](examples/weather_data.txt) of the model.


### Command-line interface

This examples shows how you can port a model from the command line. The model can be ported by using the following command:

```sh
python -m weka_porter --input <txt_file> [--output <destination_dir>] [--language {c,java,js}]
python -m weka_porter -i <txt_file> [-o <destination_dir>] [-l {c,java,js}]
```

For example:

```sh
python -m weka_porter --input model.txt --language java
python -m weka_porter -i model.txt -l java
```

By changing the language parameter you can set the target programming language:

```
python -m weka_porter -i model.txt -l java
python -m weka_porter -i model.txt -l js
python -m weka_porter -i model.txt -l c
```

Finally the following command will display all options:

```sh
python -m weka_porter --help
python -m weka_porter -h
```


## Development

### Environment

Install the required environment [modules](environment.yml) by executing the bash script [sh_environment.sh](sh_environment.sh) or type:

```sh
conda config --add channels conda-forge
conda env create -n weka-porter python=2 -f environment.yml
```

Furthermore you need to install [Node.js](https://nodejs.org) (`>=6`), [Java](https://java.com) (`>=1.6`) and [GCC](https://gcc.gnu.org) (`>=4.2`) for testing.


### Testing

Run all [tests](tests) by executing the bash script [sh_tests.sh](sh_tests.sh) or type:

```sh
source activate weka-porter
python -m unittest discover -vp '*Test.py'
source deactivate
```

The tests cover module functions as well as matching predictions of ported trees.


## Questions?

Don't be shy and feel free to contact me on [Twitter](https://twitter.com/darius_morawiec).


## License

The library is Open Source Software released under the [MIT](license.txt) license.
