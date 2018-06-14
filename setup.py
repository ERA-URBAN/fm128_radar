import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "fm128_radar",
    version = "0.1.0",
    author = "Ronald van Haren",
    author_email = "r.vanharen@esciencecenter.nl",
    description = ("A python library to convert netCDF files to WRFDA "
                    "supported fm128_radar ascii files"),
    license = "Apache 2.0",
    keywords = "WRFDA netCDF WRF radar",
    url = "https://github.com/ERA-URBAN/fm128_radar",
    packages=['fm128_radar'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: Apache Software License",
    ],
    install_requires=['numpy'],
)
