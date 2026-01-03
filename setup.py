"""Setup configuration for the demo application"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="demo-python-project",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A simple demonstration Python project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/demo-python-project",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[],
    extras_require={
        "dev": ["pytest>=7.0.0"],
    },
    entry_points={
        "console_scripts": [
            "demo-app=demo_app.main:main",
        ],
    },
)

