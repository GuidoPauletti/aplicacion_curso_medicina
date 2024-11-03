from setuptools import setup, find_packages

setup(
    name="curso_medicina",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'customtkinter',
        'mysql-connector-python',
    ],
)