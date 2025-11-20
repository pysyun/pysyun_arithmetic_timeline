from setuptools import setup, find_packages

setup(
    name='pysyun_arithmetic_timeline',
    version='1.0.1',
    author='Illia Tsokolenko',
    author_email='illiatea2@gmail.com',
    description='Storage.Timeline arithmetic operations',
    py_modules=['pysyun_arithmetic_timeline'],
    packages=find_packages(),
    install_requires=[
        'pysyun_chain @ git+https://github.com/pysyun/pysyun_chain.git'
    ]
)
