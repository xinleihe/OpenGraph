# from setuptools import setup, find_packages
# setup(
#     name="ONAP",
#     version="0.1",
#     packages=find_packages(),
# )



from setuptools import setup
from os import path

DIR = path.dirname(path.abspath(__file__))
# INSTALL_PACKAGES = open(path.join(DIR, 'requirements.txt')).read().splitlines()

with open(path.join(DIR, 'README.md')) as f:
    README = f.read()

setup(
    name='ONAP',
    packages=['ONAP'],
    description="ONAP testing",
    long_description=README,
    long_description_content_type='text/markdown',
    # install_requires=INSTALL_PACKAGES,
    version='0.0.1',
    url='https://github.com/willingnesshxl/ONAP',
    author='A B C D',
    author_email='test@gmail.com',
    keywords=['ONAP'],
    tests_require=[
        'pytest',
        'pytest-cov',
        'pytest-sugar'
    ],
    package_data={
        # include json and pkl files
        '': ['*.json', 'models/*.pkl', 'models/*.json'],
    },
    include_package_data=True,
    python_requires='>=3'
)
