from setuptools import setup, find_packages

setup(
    name="nyanja",
    version="0.1",
    packages=find_packages(),
    py_modules=["cli"],
    entry_points={
        "console_scripts": [
            "nyanja=cli:main",
        ],
    },
    install_requires=[],
)