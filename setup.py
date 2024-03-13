from setuptools import setup, find_packages

setup(
    name='hexs_rag',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'hexsrag-env=cli.py:main'
        ]
    },
    #install_requires
)
    