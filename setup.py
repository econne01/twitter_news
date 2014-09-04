from setuptools import setup, find_packages

setup(
    name = "twitter-news-flask",
    version = "0.1",
    author = 'Eric Connelly',
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    install_requires = ['setuptools'],
)
