from setuptools import setup, find_packages

setup(
    name="agent-gateway",  # Your package name on PyPI
    version="0.1.0",  # Update as needed
    description="A centralized framework to use a model of your choice for your agentic usecases.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Santosh Ameti",
    author_email="santosh.ameti@gmail.com",
    url="https://github.com/santoshameti/agent-gateway",  # Link to the GitHub repo
    license="MIT",  # Ensure this matches your LICENSE file
    packages=find_packages(exclude=["tests", "examples"]),  # Include all packages except tests and examples
    install_requires=open("requirements.txt").read().splitlines(),  # Dependencies from requirements.txt
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Update as needed
)
