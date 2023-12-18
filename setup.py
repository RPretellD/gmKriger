from setuptools import setup, find_packages, Extension

with open("README.md","r", encoding = 'utf-8') as fp:
	readme = fp.read()

setup(
	name="gmKriger",
	version="0.1.0",
	description="Kriging-based ground motion intensity measure calculator.",
	author="A. Renmin Pretell Ductram",
	author_email="rpretell@unr.edu",
	url="https://github.com/RPretellD/gmKriger",
    long_description=readme,
    
    packages=find_packages(),
	include_package_data=True,
	
    install_requires=["numpy"],

	license="MIT",
	keywords=["ground motion","Kriging","interpolation"],
	classifiers=[
        "Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
	]
)