import setuptools


with open("typehintjson/README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="typehintjson",
    version="1.0.1",
    author="Julie Ganeshan",
    author_email="HeavenlyQueen@outlook.com",
    description="Converts dataclasses / enums to JSON and back using type hints",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Sanjay-Ganeshan/typehintjson",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)