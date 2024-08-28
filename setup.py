from setuptools import setup, find_packages

setup(
    name='hexamind',
    version='v0.2',
    author='Julien Fresnel, Max Beales, Alexandre Fleutelot',
    author_email='julien.fresnel@hexamind.ai, max.beales@hexamind.ai, alexandre.fleutelot@hexamind.ai',
    description='Hexamind library',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    classifiers=[
           "Programming Language :: Python :: 3",
           "License :: OSI Approved :: MIT License",
           "Operating System :: OS Independent",
       ],
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
    
