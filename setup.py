import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setuptools.setup(
    name='AIServices',
    version='0.0.1',
    author='Ahmed badr',
    author_email='ahmed.k.badr.97@gmail.com',
    description='andalusia ai services',
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,

    url='https://github.com/Andalusia-Data-Science-Team/AIServices',
    license='MIT',
    packages=['AIServices'],
    package_dir={
        'AIServices': 'src/AIServices'},
    install_requires=['numpy', 'requests'],
)
