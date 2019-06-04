# External Libraries
from setuptools import setup

VERSION = "0.3.0"

with open("requirements.txt") as f:
    REQUIREMENTS = f.readlines()

with open("README.rst") as f:
    README = f.read()

setup(
    name="intercept.py",
    author="martmists",
    author_email="mail@martmists.com",
    maintainer="martmists",
    maintainer_email="mail@martmists.com",
    license="MIT",
    zip_safe=False,
    version=VERSION,
    description="Python library for intercept, a game by bubmet",
    long_description=README,
    url="https://github.com/martmists/intercept.py",
    packages=['intercept'],
    install_requires=REQUIREMENTS,
    keywords=["game", "intercept", "asyncio", "trio", "curio", "anyio"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Framework :: AsyncIO",
        "Topic :: Games/Entertainment",
        "Topic :: Communications :: Chat",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    python_requires=">=3.6"
)
