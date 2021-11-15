from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="govbot",
    version="0.0.1",
    author="Stephen Thoma",
    author_email="stephen@thoma.io",
    description="A twitter bot that tweets about Snapshot.org governance proposals",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/stephen_thoma/govbot",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=["requests", "tweepy", "google-cloud-firestore", "sgqlc", "pytz"],
)
