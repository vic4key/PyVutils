from setuptools import setup, find_namespace_packages

install_requires = []
with open("PyVutils/requirements.txt") as f: install_requires = f.read().split("\n")
install_requires = list(filter(lambda e: len(e) > 0, install_requires))

setup(
    name="PyVutils",
    version="1.0",
    author="Vic P.",
    author_email="vic4key@gmail.com",
    packages=find_namespace_packages(exclude=["Examples"]),
    url="https://github.com/vic4key/PyVutils.git",
    license="LICENSE",
    description="Vutils for Python",
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    install_requires=install_requires,
    include_package_data=True,
    package_data={},
)