from setuptools import setup, find_packages

setup(
    name="exponential-core",
    version="0.1.0",
    description="Librería interna compartida por los microservicios de Exponential IT",
    author="Equipo Exponential",
    packages=find_packages(include=["exponential_core", "exponential_core.*"]),
    install_requires=["fastapi", "httpx", "pydantic", "colorlog"],
    python_requires=">=3.9",
)
