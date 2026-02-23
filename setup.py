from setuptools import setup, find_packages

setup(
    name='coins_founder',
    version='0.0',
    packages=find_packages(),
    install_requires=[
        "fastapi==0.131.0",
        "httpx==0.28.1",
        "uvicorn==0.41.0"
    ]
)
