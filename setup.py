import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="repov",
    version="0.1",
    author="Amir Ehsandar",
    author_email="ehsandaramir@gmail.com",
    description="A commandline tool for validating c# assignments",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ehsandaramir/project_validator",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPL License",
        "Operating System :: OS Independent",
    ],
    entry_points={"console_scripts": ["repov = project_validator.__main__:main"]},
)
