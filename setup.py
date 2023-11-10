from setuptools import setup

setup(
    name="Testing_Assignment_1",
    version="1.0.0",
    packages=["src", "tests"],
    install_requires=["requests", "pytest", "mock", "datetime", "coverage"],
    python_requires=">=3.3",
)
