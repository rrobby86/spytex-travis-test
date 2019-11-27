from setuptools import setup, find_packages
import os
import re

def find_version():
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, "spytex", "__init__.py"), "r") as f:
        source = f.read()
    match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", source, re.M)
    if not match:
        raise RuntimeError("cannot find version string")
    return match.group(1)

setup(
    name="spytex",
    version=find_version(),
    packages=find_packages(),
    entry_points={
        "console_scripts": ["spytex=spytex.cli:main"]
    }
)
