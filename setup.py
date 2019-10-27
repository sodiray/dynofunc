import setuptools

VERSION='2.0.0'

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dynamof",
    version=VERSION,
    author="Ray Epps",
    author_email="rayharryepps@gmail.com",
    description="A small interface for more easily making calls to dynamo using boto.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rayepps/dynamof",
    download_url=f'https://github.com/rayepps/dynamof/archive/{VERSION}.tar.gz',
    packages=setuptools.find_packages(exclude="test"),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        "Operating System :: OS Independent"
    ],
    python_requires='>=3',
    install_requires=[
        'boto3',
        'botocore'
    ]
)
