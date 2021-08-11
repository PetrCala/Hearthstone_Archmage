from setuptools import setup, find_packages

setup(
    name = 'HearthstoneArchmage',
    version='0.1.0',
    packages = find_packages(),
    install_requires = [
        'PyYAML',
        'pandas>=0.23.3',
        'numpy>=1.14.5'
    ]
)


#setup(
#    name='HearthstoneArchmage',
#    version='0.1.0',
#    packages=find_packages(),
#    scripts = ['scripts/DataExtractor',
#               'scripts/DataProcessor',
#               'scripts/HearthstoneArchmage'],
#    install_requires=[
#        'PyYAML',
#        'pandas>=0.23.3',
#        'numpy>=1.14.5'
#    ],
#    setup_requires=['pytest-runner'],
#    tests_require=['pytest'],
#)