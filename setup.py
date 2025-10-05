from setuptools import setup, find_packages

setup(
    name="coin-casino",
    version="1.0.0",
    description="A feature-rich desktop casino game with multiple mini-games and progression system",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "matplotlib>=3.5.0",
    ],
    entry_points={
        "console_scripts": [
            "coin-casino=coin_casino.__main__:main",
        ],
    },
    python_requires=">=3.8",
    author="Your Name",
    author_email="your-email@example.com",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9", 
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Topic :: Games/Entertainment",
    ],
)
