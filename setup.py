"""
Satellite imagery for dummies.
"""
from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

dependencies = [
    "numpy==1.19.1",
    "click==7.1.2",
    "requests==2.24.0",
    "sat-search==0.2.3",
    "rich==3.3.2",
    "tqdm==4.48.0",
    "rasterio==1.1.5",
    "rio-color==1.0.0",
    "pillow==7.2.0",
    "opencv-python==4.3.0.36"
]

setup(
    name="felicette",
    version="0.1.2",
    url="https://github.com/plant99/felicette",
    license="BSD",
    author="Shivashis Padhi",
    author_email="shivashispadhi@gmail.com",
    description="Satellite imagery for dummies.",
    long_description=__doc__,
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    zip_safe=False,
    platforms="any",
    install_requires=dependencies,
    entry_points={"console_scripts": ["felicette = felicette.cli:main",],},
    classifiers=[
        # As from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        # 'Development Status :: 1 - Planning',
        # "Development Status :: 2 - Pre-Alpha",
        'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX",
        "Operating System :: MacOS",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
