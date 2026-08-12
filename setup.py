#!/usr/bin/env python3
"""Setup script for JARVIS."""

from setuptools import setup, find_packages

setup(
    name="jarvis-ai",
    version="0.0.01",
    description="Privacy-first AI desktop assistant",
    author="Edoardo Pensi",
    license="GNU General Public License v3.0",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "PyQt6>=6.6.1",
        "PyQt6-WebEngine>=6.6.1",
        "pynput>=1.7.6",
        "pyttsx3>=2.90",
        "vosk>=0.3.32",
        "pyaudio>=0.2.13",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
