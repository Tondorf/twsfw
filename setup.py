#!/usr/bin/env python

import os
import sys

from Cython.Build import cythonize
from setuptools import Extension, find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))
sys.path.append(here)

import versioneer  # noqa: E402

with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()


setup(
    name="twsfw",
    description="The W stands for WASM",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tondorf/twsfw",
    author="Happy Twondorfler",
    author_email="",  # TODO
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    packages=find_packages(exclude=["docs", "tests"]),
    python_requires=">=3.12",
    install_requires=["wasmtime"],
    extras_require={
        "dev": [
            "pre-commit",
            "pytest",
            "pytest-cov",
            "sphinx",
        ],
    },
    ext_modules=cythonize(
        [
            Extension(
                "twsfwphysx",
                sources=[os.path.join(here, "twsfwphysx", "binding.pyx")],
                include_dirs=[
                    os.path.join(here, "twsfwphysx", "twsfwphysx", "include")
                ],
                extra_compile_args=["-DTWSFWPHYSX_IMPLEMENTATION"],
            )
        ]
    ),
    entry_points={
        "console_scripts": [
            "twsfw = twsfw.__main__:main",
        ]
    },
)
