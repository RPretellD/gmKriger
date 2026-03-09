from setuptools import setup, find_packages, Extension

with open("README.md","r", encoding = 'utf-8') as fp:
    readme = fp.read()

# Call setup
setup(
    name="gmKriger",
    version="1.0.0",

    description="Kriging-based ground motion intensity measure calculator.",
    author="Renmin Pretell",
    author_email="rpretell@unr.edu",
    url="https://github.com/RPretellD/gmKriger",
    
    long_description_content_type="text/markdown",
    long_description=readme,
    
    packages=find_packages(),

    include_package_data=True,

    classifiers=[
        "Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
	]
)