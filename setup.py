from distutils.core import setup

setup(
    name='cronofy',
    version='0.0.1',
    author='Nik Brbora',
    author_email='nik@saberr.com',
    packages=['cronofy', 'cronofy.test'],
    url='http://www.example.com',
    license='MIT',
    description='Cronofy Python SDK',
    long_description='README.md',
    install_requires=[
        "requests >= 2.5.3"
    ],
)