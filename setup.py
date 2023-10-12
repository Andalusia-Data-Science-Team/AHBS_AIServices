import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setuptools.setup(
    name='AHBS_AIServices',
    version='0.0.33',
    author='Ahmed badr',
    author_email='ahmed.k.badr.97@gmail.com',
    description='andalusia ai services',
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,

    url='https://github.com/Andalusia-Data-Science-Team/AHBS_AIServices',
    license='MIT',
    packages=['AHBS_AIServices'],
    package_dir={
        'AHBS_AIServices': 'src/AHBS_AIServices'},
    install_requires=['numpy', 'requests','chardet'],
)
