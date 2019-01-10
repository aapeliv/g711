from setuptools import setup

with open("readme.md", "r") as fh:
    long_description = fh.read()

setup(
    name = "g711",
    version="0.0.1",
    author="Aapeli Vuorinen",
    author_email="python@aapelivuorinen.com",
    description="A G.711 encoding and decoding tool.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aapeliv/g711",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Topic :: Communications :: Telephony",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
        "Intended Audience :: Telecommunications Industry",
        "Intended Audience :: Customer Service",
    ],
    setup_requires = ["cffi>=1"],
    cffi_modules=["python_bindings/python_g711.py:ffibuilder"],
    install_requires = ["cffi>=1"],
)
