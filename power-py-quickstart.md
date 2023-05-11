# Power BI Python Quickstart

## Creating a wheel
To deploy the wheel you will need to package the exiting code base as a Python wheel. To do this you will need a Python package called setuptools.

```
pip install setuptools
```
Once you have pip installed setuptools you can build the package and deploy.

Open a cmd window and navigate to the folder which contains the "power-py".

```
cd "C:\Users\[user]\source\repos\power-py"
```

From here you will then need to build the package.

```
Python setup.py sdist bdist_wheel
```
