from setuptools import setup, find_packages

print(find_packages())

setup(
    name="agentgateway",  # Your package name on PyPI
    version="1.1.1",  # Update as needed
    description="A centralized framework to use a model of your choice for your agentic usecases.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Santosh Ameti",
    author_email="santosh.ameti@gmail.com",
    url="https://github.com/santoshameti/agentgateway",  # Link to the GitHub repo
    license="MIT",  # Ensure this matches your LICENSE file
    packages=find_packages(),
    include_package_data=True,    # Include data files specified in MANIFEST.in
    install_requires=open("requirements.txt").read().splitlines(),  # Dependencies from requirements.txt
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Update as needed
    package_data={
        '': ['config.yaml'],  # Include config.yaml in the root of the package
    },
)
