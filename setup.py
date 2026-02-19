from setuptools import setup, find_packages

setup(
    name="kayzendb",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "cryptography",
    ],
    entry_points={
        "console_scripts": [
            "kayzen=kayzendb.cli:main",
        ],
    },
    author="Kayzen Architect",
    description="A secure, lightweight, ACID-lite file-based database.",
)
