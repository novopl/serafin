import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="igor-serialize",
    version=read('VERSION').strip(),
    author="Mateusz 'novo' Klos",
    author_email="novopl@gmail.com",
    license="MIT",
    keywords="igor-serialize serialize serialization json config",
    url="http://github.com/novopl/igor-urlconf",
    description="Standalone URL dispatcher implementation",
    packages=[
        'igor.serialize',
    ],
    install_requires=[
        'igor-core',
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
    ],
)
