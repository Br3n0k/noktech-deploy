from setuptools import setup, find_packages

setup(
    name="noktech-deploy",
    version="0.1.0",
    description="Cliente de deploy avançado com suporte a múltiplos protocolos e observação de mudanças em tempo real",
    author="Brendown Ferreira",
    author_email="br3n0k@gmail.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "paramiko>=2.8.1",
        "watchdog>=2.1.9",
        "typing-extensions>=4.4.0"
    ],
    entry_points={
        'console_scripts': [
            'noktech-deploy=src.deploy_client:main',
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Build Tools",
        "Topic :: System :: Software Distribution",
    ],
    python_requires=">=3.8",
) 