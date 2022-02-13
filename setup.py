from distutils.core import setup

setup(
    name='velero-velero-bot-sdk',
    version='0.62.3',
    packages=[
        'velero_bot_sdk',
    ],
    url='https://github.com/velerofinance/velero-velero-bot-sdk.git',
    license='',
    author='velerofinance',
    author_email='imdipperpines3199@gmail.com',
    description='',
    install_requires=[
        'httplib2==0.20.4',
        'oauth2client~=4.1.3',
        'google-api-python-client==2.36.0',
        'tornado==6.1',
        'web3==5.27.0',
        'pymongo==4.0.1',
        'gunicorn==20.1.0',
    ],
)