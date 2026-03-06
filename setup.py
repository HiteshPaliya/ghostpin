"""
GhostPin v5.0 — setup.py
"""
from setuptools import setup, find_packages

setup(
    name='ghostpin',
    version='5.0.0',
    description='Enterprise SSL Pinning Bypass & Mobile Security Testing Platform',
    author='GhostPin Security',
    packages=find_packages(),
    python_requires='>=3.8',
    install_requires=[
        'flask>=2.0',
        'click>=8.0',
        'requests>=2.28',
        'frida-tools>=12.0.0',
        'objection>=1.11.0',
        'mitmproxy>=10.0.0',
    ],
    entry_points={
        'console_scripts': [
            'ghostpin=ghostpin.cli:cli',
        ],
    },
    package_data={
        'ghostpin': ['scripts/**/*.js'],
    },
)
