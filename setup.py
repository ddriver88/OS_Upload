from setuptools import setup, find_packages

setup(
    name="my_application",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "streamlit",
        "pandas",
    ],
)