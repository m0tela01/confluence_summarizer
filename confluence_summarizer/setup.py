"""Setup script for the Confluence Summarizer package."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="confluence-summarizer",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Generate summaries of Confluence content using Azure OpenAI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/confluence-summarizer",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Documentation",
        "Topic :: Text Processing :: Markup",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    install_requires=[
        "click>=8.0.0",
        "rich>=10.0.0",
        "atlassian-python-api>=3.0.0",
        "langchain>=0.1.0",
        "langchain-core>=0.1.0",
        "openai>=1.0.0",
        "pyyaml>=6.0.0",
        "python-dotenv>=1.0.0",
        "typing-extensions>=4.0.0",
        "pydantic>=2.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "isort>=5.0.0",
            "mypy>=1.0.0",
            "flake8>=6.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "confluence-summarizer=confluence_summarizer.cli:cli",
        ],
    },
    include_package_data=True,
    package_data={
        "confluence_summarizer": ["config/*.yaml"],
    },
) 