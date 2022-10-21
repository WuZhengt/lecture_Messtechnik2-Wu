import setuptools


setuptools.setup(
    name="lecture-tools-Markus-Gardilll", # Replace with your own username
    version="0.0.1",
    author="Markus Gardill",
    author_email="markus.gardill@uni-wuerzburg.de",
    description="A package providing common tools for lecture content.",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    requires=['docopt>=0.6']
    python_requires='>=3.6',
)