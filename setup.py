from setuptools import setup, find_packages

import subprocess
import sys

subprocess.run(
    ["bash parser/build.sh"], stdout=sys.stdout, stderr=sys.stderr,
    shell=True,
)

setup(
    name='codeaug',
    version='0.1.0',    
    description='A project for code augmentations',
    url='TBD',
    author='Sergey Troshin',
    author_email='serj.troshin2013@yandex.ru',
    license='BSD 2-clause',
    packages=find_packages("."),
    include_package_data=True,
    install_requires=[
       "tree-sitter==0.19.0",
       "pygments==2.7.1",
       "sacrebleu==1.2.11",
    ],

    classifiers=[
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)