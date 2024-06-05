from setuptools import setup, find_packages

setup(
    name='hexamind',
    version='0.1',
    author='Julien Fresnel, Max Beales',
    author_email='julien.fresnel@hexamind.ai, max.beales@hexamind.ai',
    description='Hexamind library to implement RAG solutions',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'hexamind-env=cli.py:main'
        ]
    },
    python_requires='>=3.12',
)
    