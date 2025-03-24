from setuptools import setup, find_packages

setup(
    name="task-queue",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi==0.109.2",
        "uvicorn==0.27.1",
        "redis==5.0.1",
        "pytest==8.0.2",
        "pytest-asyncio==0.23.5",
        "httpx==0.26.0",
    ],
)
