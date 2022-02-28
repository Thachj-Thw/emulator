from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='emulator',
    version='0.0.1',
    description='package help control emulator',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Thachj-Thw/emulator',
    author='Thw',
    author_email='',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Natural Language :: Vietnamese'
    ],
    keywords='emulator, android, android emulator',
    packages=['emulator'],
    python_requires='>=3.6',
    include_package_data=True,
    project_urls={
        'Source': 'https://github.com/Thachj-Thw/emulator',
    },
)
