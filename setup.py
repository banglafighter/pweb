from setuptools import setup, find_packages
import os
import pathlib

CURRENT_DIR = pathlib.Path(__file__).parent
README = (CURRENT_DIR / "README.md").read_text()

env = os.environ.get('source')


def get_dependencies():
    dependency = ["Flask==3.0.0", "Flask-Cors==4.0.0"]

    if env and env == "code":
        return dependency

    return dependency + ["ppy-common", "pweb-orm", "pweb-form-rest", "pweb-cli", "ppy-jsonyml"]


setup(
    name='pwebb',
    version='0.0.6',
    url='https://github.com/banglafighter/pweb',
    license='Apache 2.0',
    author='Bangla Fighter',
    author_email='banglafighter.com@gmail.com',
    description='Python Web Boot (PWebB). PWebB is a DRY full-stack framework based on Flask micro web framework.',
    long_description=README,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    entry_points={'console_scripts': ['pweb=pweb_app:cli']},
    install_requires=get_dependencies(),
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
    ]
)
