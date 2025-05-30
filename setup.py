from setuptools import setup, find_packages

setup(
    name="cobaltmirror-enrichment",
    version="0.1.0",
    description="OSINT NLP enrichment pipeline (NER, geolocation, time)",
    author="Your Name",
    author_email="you@example.com",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "spacy>=3.0",
        "geopy>=2.2",
        "dateparser>=1.1",
        "click>=8.0"
    ],
    entry_points={
        "console_scripts": [
            "cobaltmirror-enrich = cobaltmirror_enrichment.cli:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
