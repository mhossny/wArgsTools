#!/Users/mo/anaconda3/bin/python
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wArgsTools",
    version="0.1.1",
    author="Mo Hossny",
    author_email="mhossny@ieee.org",
    description="A wrapping tool to inspect and exports callable args into an argparse parser",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mhossny/wArgsTools.git",
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',      # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["docutils>=0.3", "argparse", "numpy"],
    python_requires='>=3.6',
)
