import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="idynamo",
    version="0.0.1",
    author="Ray Epps",
    author_email="rayharryepps@gmail.com",
    description="A small interface for more easily making calls to dynamo using boto.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rayepps/idynamo",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
