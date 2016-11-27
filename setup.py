import os
from setuptools import setup, find_packages

from weka_porter import Porter
VERSION = Porter.__version__

path = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(path, 'requirements.txt')) as f:
    all_reqs = f.read().split('\n')
install_requires = [x.strip() for x in all_reqs if 'git+' not in x]

setup(
    name='weka-porter',
    packages=find_packages(exclude=["tests.*", "tests"]),
    include_package_data=True,
    version=VERSION,
    description='Transpile trained decision trees from Weka to a low-level programming language.',
    author='Darius Morawiec',
    author_email='ping@nok.onl',
    url='https://github.com/nok/weka-porter/tree/stable',
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    install_requires=install_requires,
    keywords=['weka', 'decision-tree'],
    license='MIT',
)
