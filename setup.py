"""
SaraAI Max — Installation
Run: pip install -e .
Then use: sara  (from anywhere in terminal)
"""

from setuptools import setup, find_packages

setup(
    name="sara-ai-max",
    version="1.0.0",
    author="Selva Pandi",
    author_email="selva.ux@yahoo.com",
    description="SaraAI Max — Next-Gen Autonomous Intelligence powered by Ollama",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/SelvaUx/SaraAI",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "requests>=2.28.0",
        "rich>=13.0.0",
        "psutil>=5.9.0",
        "pyautogui>=0.9.54",
        "Pillow>=9.0.0",
    ],
    extras_require={
        "voice": [
            "pyttsx3>=2.90",
            "SpeechRecognition>=3.10.0",
            "pyaudio>=0.2.13",
        ],
    },
    entry_points={
        "console_scripts": [
            "sara=sara.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
