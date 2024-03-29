"""Collection of tools I used reapatedly in Python 
(but they do not deserve a stand-alone repo :)
"""

from setuptools import setup, find_packages


INSTALL_REQUIRES = [
    'pytest',
    'pandas',
    'SQLAlchemy',
    'PyMySQL',
    'python-dotenv'
]


setup(
    name = "mmpy_tools",
    version = "0.2.4",
    description = "Collection of tools I used reapatedly in Python",
    author = "Michal Mikolaj",
    packages = find_packages(),
    zip_safe = False,
    install_requires=INSTALL_REQUIRES
)
