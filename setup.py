from setuptools import setup, find_packages

from glob import glob
from os.path import basename
from os.path import splitext

setup(
    name='aws_connector',
    version='0.0.1',
    packages=find_packages('src', exclude=('tests', 'docs')),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    setup_requires=['pytest-runner',],
    tests_require=['pytest',],
    include_package_data=True,
    zip_safe=False,
)
