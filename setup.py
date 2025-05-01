from setuptools import setup, find_packages

setup(
    name="mycomonitor",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "RPi.GPIO>=0.7.0",
        "click>=8.0.0",
        "Flask>=2.0.0",
        "requests>=2.25.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-mock>=3.10.0",
            "pytest-cov>=4.0.0",
            "black>=22.3.0",
            "isort>=5.10.1",
            "mypy>=1.0.0",
            "flake8>=4.0.1",
        ],
    },
    entry_points={
        'console_scripts': [
            'mycomonitor=mycomonitor.cli.commands:cli',
            'mycomonitor-web=mycomonitor.web.app:create_app',
        ],
    },
    python_requires=">=3.9",
    author="Aaron Jacobs",
    author_email="git@happycaps.co.uk",
    description="Automated mushroom growing environment controller using Raspberry Pi",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/aaronjacobs-chelt/Raspberry-PI-Automated-Mushroom-Farm",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Home Automation",
    ],
)
