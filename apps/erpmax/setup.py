# ERPMAX Setup Configuration
from setuptools import setup, find_packages
import re, ast

# get version from __version__ variable in erpmax/__init__.py
_version_re = re.compile(r'__version__\s+=\s+(.*)') 

with open('erpmax/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

requirements = []

setup(
    name='erpmax',
    version=version,
    description='Enhanced ERP solution built on ERPNext with modern features',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='ERPMAX Team',
    author_email='info@erpmax.com',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=requirements,
    python_requires='>=3.8',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Framework :: ERPNext",
        "Topic :: Office/Business :: Financial :: Accounting",
        "Topic :: Office/Business :: Enterprise Resource Planning",
    ],
    keywords="erpnext erp business accounting inventory",
    project_urls={
        "Documentation": "https://github.com/yourusername/erpmax/wiki",
        "Source": "https://github.com/yourusername/erpmax",
        "Tracker": "https://github.com/yourusername/erpmax/issues",
    },
)
