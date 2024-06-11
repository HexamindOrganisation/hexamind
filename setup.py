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
            'hexamind-env=hexamind.cli:main'
        ]
    },
    python_requires='>=3.10',
    install_requires=[
        'beautifulsoup4==4.12.3',
        'chromadb==0.5.0',
        'elasticsearch==8.12.1',
        'mistralai==0.3.0',
        'openai==1.31.0',
        'python_docx==1.1.0',
        'Requests==2.32.3',
        'setuptools==68.2.2',
        "mammoth==1.7.1"
    ]
)
    