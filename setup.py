from pathlib import Path

import setuptools

from pynction.version import __version__

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setuptools.setup(
    name="pynction",
    version=__version__,
    license="MIT",
    author="Nicolas Nunez",
    author_email="nicolas110996@gmail.com",
    packages=setuptools.find_packages(),
    url="https://github.com/niconunez96/pynction",
    description="Functional based library to support monads and other functional programming concepts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development",
        "Topic :: Utilities",
    ],
    python_requires=">=3.7",
)
