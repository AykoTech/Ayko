#!/usr/bin/env python3
"""
AYKO v0.0.01 - Desktop AI Coworker
GNU General Public License v3.0
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ayko",
    version="0.0.01",
    author="Edoardo Pensi",
    description="Desktop AI Coworker - Local, privacy-first voice assistant",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/edoardo-pensi/ayko",
    license="GNU General Public License v3.0",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        # Core Audio/LLM
        "vosk==0.3.45",
        "sounddevice==0.4.6",
        "requests==2.31.0",
        "pyttsx3==2.90",

        # UI & Desktop
        "PyQt6==6.7.1",
        "PyQt6-WebEngine==6.7.1",

        # System & Utilities
        "psutil==5.9.8",
        "pynput==1.7.6",
        "python-dotenv==1.0.0",
        "Pillow==10.1.0",
    ],
    extras_require={
        "dev": [
            "pytest==7.4.3",
            "pytest-cov==4.1.0",
            "pytest-qt==4.2.0",
        ],
    },
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: X11 Applications :: Qt",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: Italian",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Home Automation",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
    ],
    entry_points={
        "console_scripts": [
            "ayko=src.main:main",
        ],
    },
)
