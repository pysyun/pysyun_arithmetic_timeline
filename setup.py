from setuptools import setup, find_packages

setup(
    name='pysyun_arithmetic',
    version='1.0.0',
    author='Illia Tsokolenko',
    author_email='illiatea2@gmail.com',
    description='Arithmetic operations for time series data processing',
    py_modules=['pysyun_arithmetic'],
    packages=find_packages(),
    install_requires=[
        'pysyun_chain @ git+https://github.com/pysyun/pysyun_chain.git'
    ]
)
