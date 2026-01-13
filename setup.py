# networksecurity/setup.py
import os
from setuptools import setup, find_packages
from typing import List

def get_requirements() -> List[str]:
    req_file = os.path.join(os.path.dirname(__file__), "requirements.txt")
    reqs = []
    if os.path.exists(req_file):
        with open(req_file) as f:
            for line in f:
                req = line.strip()
                if req and req != "-e .":
                    reqs.append(req)
    return reqs

setup(
    name="networksecurity",
    version="0.0.1",
    author="Tanmay Somkuwar",
    author_email="tanmaysomkuwar60@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements(),
    python_requires=">=3.8",
)