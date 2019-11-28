from setuptools import setup, find_packages
import os
import re

basedir = os.path.abspath(os.path.dirname(__file__))

def file(*path):
    return os.path.join(basedir, *path)

def get_long_description():
    with open(file("README.md"), "r") as f:
        return f.read()

def find_version():
    with open(file("spytex", "__init__.py"), "r") as f:
        source = f.read()
    match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", source, re.M)
    if not match:
        raise RuntimeError("cannot find version string")
    return match.group(1)

setup(
    name="spytex",
    version=find_version(),
    author="rrobby86",
    author_email="rrobby86@gmail.com",
    description="Run arbitrary Python functions indicated by JSON specs",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/rrobby86/spytex",
    packages=find_packages(),
    install_requires=[
        "smart-open>=1.8.1",
    ],
    entry_points={
        "console_scripts": ["spytex=spytex.cli:main"]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
