from setuptools import setup, find_packages

setup(
    name = 'HearthstoneArchmage',
    version='0.1.1',
    packages = find_packages(),
    install_requires = [
        'PyYAML',
        'pandas>=0.23.3',
        'numpy>=1.14.5',
        'selenium>=3.141.0',
        'PySimpleGUI>=4.46.0',
        'pywin32',
        'openpyxl>=3.0.7' #Excel opening
    ],
    setup_requires = ['pytest-runner'],
    tests_require=['pytest']
)

#Install using 'pip install --editable .'

#Maybe 'py setup.py build'? or smth