# from setuptools import setup, find_packages
# setup(
#     name="ONAP",
#     version="0.1",
#     packages=find_packages(),
# )



from setuptools import setup
from os import path


def read_requirements(filename):
    return [line.strip() for line in read_file(filename).splitlines()
            if not line.startswith('#')]

DIR = path.dirname(path.abspath(__file__))
# INSTALL_PACKAGES = open(path.join(DIR, 'requirements.txt')).read().splitlines()

with open(path.join(DIR, 'README.md')) as f:
    README = f.read()




setup(
    name='OpenGraph',
    packages=['OpenGraph','OpenGraph/classes','OpenGraph/functions','OpenGraph/tests','OpenGraph/utils','OpenGraph/functions/community','OpenGraph/functions/components','OpenGraph/functions/graph_embedding','OpenGraph/functions/not_sorted','OpenGraph/functions/structural_holes','OpenGraph/functions/graph_embedding/node2vec'],
    description="ONAP testing",
    long_description=README,
    long_description_content_type='text/markdown',
    # install_requires=INSTALL_PACKAGES,
    version='0.0.4',
    license="MIT",
    url='https://github.com/willingnesshxl/OpenGraph',
    author='A, B, C, D',
    author_email='OpenGraph@163.com',
    keywords=['OpenGraph'],
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
    python_requires='>=3',
    install_requires = ['gensim==3.8.1', #'numpy==1.18.1'
    ],
)
