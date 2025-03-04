from setuptools import setup, find_packages

setup(
    name="curso_medicina",
    version="0.8",
    packages=find_packages(),
    install_requires=[
        'customtkinter',
        'mysql-connector-python',
        'tkcalendar'
    ],
)