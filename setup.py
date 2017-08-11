
from setuptools import setup

def _readme():
    with open("README.md", "r") as read_file:
        return read_file.read()

setup(
    name="demoCampubinWagtail",
    description="A website demonstrating Campus Publication using Wagtial and digcollretriever",
    long_description=_readme(),
    packages=['demoCampubinWagtail'],
    install_requires=['wagtail', 'pytest']
)