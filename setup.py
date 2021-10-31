from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="gov_bot",
    version="0.0.1",
    author="Stephen Thoma",
    author_email="stephen@thoma.io",
    description="A twitter bot that tweets about Snaphsot.org governance proposals",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/stephen_thoma/gov-bot",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=["requests", "tweepy", "google-cloud-firestore"],
)
