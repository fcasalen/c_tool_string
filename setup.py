from setuptools import setup, find_packages

name = "c_tool_string"
version = "0.1.3"

setup(
    name=name,
    version=version,
    license="GNU General Public License",
    author="fcasalen",
    author_email="fcasalen@gmail.com",
    description="check for strings in py files in a directory. In CLI is possible to check in a given directory or in the current_directory",
    packages=find_packages(),
    include_package_data=True,
    install_requires=open('requirements.txt').readlines(),
    long_description=open("README.md").read(),
    classifiers=[
        "Development Status :: 5 - Prodution/Stable",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.12"
    ],
    entry_points={ "console_scripts": [
        "c_tool_string=c_tool_string.run:cli"
    ]}
)
