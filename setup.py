from setuptools import setup, find_packages

setup(
    name="slidepyv6",
    version="0.1.0",    
    author="Edwin Arevalo",
    author_email="terrioingeniera@gmail.com",
    description="Librería para leer y analizar archivos de proyectos geotécnicos en formato .SLIM de Slide V6 (Rocscience)",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/edwinar13/SlidePyV6-Library",  # Cambia esto por la URL de tu repositorio
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=[],
)


