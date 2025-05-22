from setuptools import setup, find_packages

setup(
    name="mvcp",
    version="0.1.0",
    description="Model Version Control Protocol - Git-compatible version control for AI agent workflows",
    author="MVCP Team",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "mvcp=mvcp.cli:main",
        ],
    },
    install_requires=[
        "click",
        "colorama",
        "pyyaml",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Version Control",
    ],
) 