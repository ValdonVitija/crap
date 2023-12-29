import setuptools

install_requires = []
with open("requirements.txt", "r", encoding="UTF-8") as f_stream:
    for pack in f_stream:
        install_requires.append(pack)


setuptools.setup(
    name="just-crap",
    version=open("VERSION").read().strip(),
    packages=setuptools.find_packages(include=["crap", "crap.*"]),
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Valdon Vitija",
    author_email="valdonvitijaa@gmail.com",
    license="MIT",
    install_requires=install_requires,
    entry_points={
        "console_scripts": [
            "crap=crap.cli:get_app",
        ],
    },
    package_data={"crap": ["data/*"]},
)
