from setuptools import setup, find_packages


setup(
    name='indefibank-bot-sdk',
    version='0.62',
    packages=find_packages(),
    url='https://github.com/indefibank/indefibank-bot-sdk.git',
    license='MIT License',
    author='captain13128',
    author_email='imdipperpines3199@gmail.com',
    description='',
    install_requires=[
        'web3==6.4.0',
        'hexbytes==0.3.1',
        'requests==2.31.0',
    ],
)
