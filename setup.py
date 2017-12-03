import setuptools

with open('README.rst') as fp:
    long_description = fp.read()

setuptools.setup(
    name='caparg',
    license='MIT',
    description="Captain Arguments: Ready for subcommand",
    long_description=long_description,
    use_incremental=True,
    setup_requires=['incremental'],
    author="Moshe Zadka",
    author_email="zadka.moshe@gmail.com",
    packages=setuptools.find_packages(where='src'),
    package_dir={"": "src"},
    install_requires=['attrs', 'incremental', 'pyrsistent'],
)
