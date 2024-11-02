from setuptools import find_packages, setup

setup(
    name="energy_mix",
    packages=find_packages(exclude=["energy_mix_tests"]),
    install_requires=["dagster", "dagster-cloud"],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
