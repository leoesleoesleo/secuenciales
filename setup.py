# setup.py
from setuptools import setup, find_packages

setup(
    name='secuenciales',
    version='0.1',
    description='Un script para ejecutar secuencialmente los JOBS',
    author='Leonardo GBM',
    packages=find_packages(),
    install_requires=[
        # Lista de dependencias si las hay
    ],
    scripts=['secuenciales.py'],
    data_files=[('', ['secuencial.json'])],
    license='MIT',
    url='https://github.com/leoesleoesleo/secuenciales',
)
