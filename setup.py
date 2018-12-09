from setuptools import setup
setup(
    name = "g711",
    setup_requires = ["cffi>=1"],
    cffi_modules=["python_g711.py:ffibuilder"],
    install_requires = ["cffi>=1"],
)