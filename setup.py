from setuptools import setup, find_packages

setup(
        name="mlops_project",
        version="0.1.0",
        packages=find_packages(),
        install_requires=[
            "pydantic>=2.0.0",
            "pytest-cov>=4.0.0",
        ]
)