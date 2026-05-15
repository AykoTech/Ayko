#!/usr/bin/env python3
"""
JARVIS v0.0.01 - Setup Script
Licensed under GNU General Public License v3.0
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_path = Path(__file__).parent / "README.md"
long_description = ""
if readme_path.exists():
    long_description = readme_path.read_text()

setup(
    name='jarvis-ai',
    version='0.0.01',
    author='Edoardo Pensi',
    author_email='contact@edoardopensi.dev',
    description='JARVIS - Desktop AI Assistant for Tony Stark (inspired)',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/edoardopensi/jarvis-ai',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    python_requires='>=3.10',
    install_requires=[
        'PyQt6>=6.6.0',
        'PyQtWebEngine>=6.6.0',
        'sounddevice>=0.4.6',
        'soundfile>=0.12.1',
        'vosk>=0.3.21',
        'pyttsx3>=2.90',
        'requests>=2.31.0',
        'psutil>=5.9.6',
        'pyautogui>=0.9.54',
        'python-dotenv>=1.0.0',
        'Pillow>=10.1.0',
        'numpy>=1.24.3',
        'pydantic>=2.5.0',
        'python-json-logger>=2.0.7',
    ],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'black>=23.0.0',
            'flake8>=6.0.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'jarvis=src.main:main',
        ],
    },
    include_package_data=True,
    package_data={
        'assets': ['*.html', '*.png'],
        'config': ['*.json'],
    },
)
