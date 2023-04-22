from setuptools import setup

setup(
    name="sparkbadge",
    author="Nick Shannon",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: MIT",
        "Programming Language :: Python",
        "Operating System :: Linux",
    ],
    description="A library and command-line tool for generating Github-style " +
    "badges",
    keywords="github badge shield status longitudinal metrics",
    python_requires=">=3.10",
    # install_requires=["Jinja2>=3,<4", "requests>=2.22.0,<3"],
    # extras_require={
    #     "pil-measurement": ["Pillow>=6,<10"],
    #     "dev": [
    #         "Flask>=2.0",
    #         "fonttools>=3.26",
    #         "nox",
    #         "Pillow>=5",
    #         "pytest>=3.6",
    #         "xmldiff>=2.4"
    #     ],
    # },
    license="MIT",
    packages=["sparkbadge"],
    url="https://github.com/klaeufer/sparkbadge")
