# TODO: Remove this file when  v15.0.0 is released
from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")
	
from erpnext import __version__ as version
name = "erpnext"

setup(
	name="erpnext",
	version=version,
	description="Frappe/ERPNext",
	author="erpnext",
	author_email="erpnext@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
