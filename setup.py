from setuptools import setup, find_namespace_packages

setup(
    name='address_assistant',
    version='1.0.0',
    description='Program for working with address and note books',
    url='https://github.com/Dimasta22/Group_6_project',
    author="Dnipro's boys team",
    author_email='serdyuk@gmail.com',
    license='Apache',
    classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
    ],
    packages=find_namespace_packages(),
    entry_points={'console_scripts': [
        'address=all_files.main:main']}
)