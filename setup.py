import os
from setuptools import setup, find_packages




def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()




# Function to read requirements from requirements.txt
def parse_requirements(filename):
    with open(filename, 'r') as f:
        return f.read().splitlines()


setup(
    name='raggenie',
    version='0.0.1',
    author='sirocco ventures',
    author_email='info@siroccoventures.com',
    description='Raggenie is a platform for easy RAG building and integration.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/sirocco-ventures/raggenie",
    license='MIT',
    packages=find_packages(),
    install_requires=parse_requirements('requirements.txt'),  # Pulls dependencies from requirements.txt
)