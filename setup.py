from setuptools import setup, find_packages

setup(
    name="novelGPT",
    version="1.0.0",
    author="Alex Cerullo",
    author_email="cerulloalexandre@gmail.com",
    description="Novel Writing GPT for Large Projects",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/AlexCerullo",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "openai",
        "python-dotenv",
    ],
)