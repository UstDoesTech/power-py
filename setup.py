import setuptools

with open("power-py-quickstart.md", "r") as fh:
    long_description = fh.read()

def main():
    "Executes the setup function"
    import power_py as app

    setuptools.setup(
        name=app.__project__,
        version=app.__version__,
        author="Ust Oldfield",
        author_email="power-py@ustdoes.tech",
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

if __name__ == "__main__":
    main()
