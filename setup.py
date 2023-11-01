from setuptools import setup
import pathlib
import shutil
import sys
import os


here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

if sys.argv[-1] == 'update':
    if os.path.isdir('dist'):
        shutil.rmtree('dist')
    if os.path.isdir('emulator_Thw.egg-info'):
        shutil.rmtree('emulator_Thw.egg-info')
    os.system('python -m build')
    os.system('twine upload dist/*')
    sys.exit()


setup(
    name='emulator-Thw',
    version='0.0.9',
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
    install_requires=['numpy', 'opencv-python'],
    python_requires='>=3.6',
    include_package_data=True,
    project_urls={
        'Source': 'https://github.com/Thachj-Thw/emulator',
    },
)
