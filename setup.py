import setuptools

with open("power-py-quickstart.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="power-py",
    version="0.0.1-1",
    author="Ust Oldfield",
    author_email="ust@ustdoes.tech",
    description="Power BI Python SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=["msal", "requests"],
)
