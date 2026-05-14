from setuptools import setup, find_packages

setup(
    name="personal-dictionary",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "kiwipiepy>=0.15.0",
    ],
    author="Antigravity",
    description="A universal custom dictionary manager for Kiwi morphological analyzer",
)
