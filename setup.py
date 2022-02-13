from distutils.core import setup

setup(
    name='velero-bot-sdk',
    version='0.63.3',
    packages=[
        'velero_bot_sdk',
    ],
    url='https://github.com/velerofinance/velero-bot-sdk.git',
    license='',
    author='velerofinance',
    author_email='imdipperpines3199@gmail.com',
    description='',
    install_requires=[
        'web3==5.28.0',
        'hexbytes~=0.2.2',
        'requests~=2.27.1',
    ],
)
