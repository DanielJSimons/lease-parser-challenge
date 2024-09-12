from setuptools import setup, find_packages

setup(
    name='lease-parser',
    version='1.0.0',
    packages=find_packages(include=['src', 'src.*']),
    install_requires=[
        'Flask>=3.0.3',
        'numpy>=2.1.1',
        'opencv-python>=4.8.1.78',
        'pandas>=2.2.2',
    ],
    extras_require={
        'dev': ['pytest', 'pytest-cov'],
    },
    entry_points={
        'console_scripts': [
            'lease-parser=src.main:main',  # Command line command to run the main function
        ],
    },
    python_requires='>=3.11',  # Built and tested on 3.11.9
)
