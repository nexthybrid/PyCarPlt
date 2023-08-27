from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="PyCarPlt",
    version="0.1.0",
    author="Tong Zhao",
    author_email="zhao.1991@osu.edu",
    description="Plotting tools for 2D vehicle dynamics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nexthybrid/PyCarPlt",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
