from setuptools import setup, find_packages

setup(
    name="exponential-core",
    version="0.1.1",
    description="Librería interna compartida por los microservicios de Exponential IT",
    author="Equipo Exponential",
    author_email="jhon.rincon@exponentialit.net",
    url="https://github.com/JohnRSantamaria/exponentail_core",
    packages=find_packages(include=["exponential_core", "exponential_core.*"]),
    # Dependencias mínimas
    install_requires=[
        "fastapi>=0.95",
        "httpx>=0.23",
        "pydantic>=2.0",
        "colorlog>=6.0",
    ],
    # Evita errores si usas datos adicionales en MANIFEST.in
    include_package_data=True,
    # Requiere Python 3.9+
    python_requires=">=3.9",
    # Clasificadores opcionales
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
