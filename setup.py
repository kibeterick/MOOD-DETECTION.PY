"""
Setup script for Mood Detection System
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="mood-detection-system",
    version="2.0.0",
    author="Kibet Erick",
    author_email="",
    description="Real-time mood detection using facial recognition and voice analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kibeterick/MOOD-DETECTION.PY",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Healthcare Industry",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Image Recognition",
        "Topic :: Multimedia :: Video :: Capture",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "mood-detect=web_mood_app:main",
            "mood-detect-cli=enhanced_main:main",
        ],
    },
    keywords=[
        "mood detection",
        "emotion recognition",
        "facial recognition",
        "voice analysis",
        "computer vision",
        "machine learning",
        "opencv",
        "flask",
        "sentiment analysis",
    ],
    project_urls={
        "Bug Reports": "https://github.com/kibeterick/MOOD-DETECTION.PY/issues",
        "Source": "https://github.com/kibeterick/MOOD-DETECTION.PY",
        "Documentation": "https://github.com/kibeterick/MOOD-DETECTION.PY/blob/main/README.md",
    },
)
