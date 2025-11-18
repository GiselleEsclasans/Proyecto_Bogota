from setuptools import setup, find_packages

setup(
    name="proyecto_bogota",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "networkx>=3.0",
        "matplotlib>=3.5",
        "numpy>=1.21",
    ],
    entry_points={
        'console_scripts': [
            'bogota-routes=src.main:main',
        ],
    },
)