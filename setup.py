from distutils.core import setup

exec(open('country_converter/version.py').read())

setup(
    name='country_converter',
    description=(
        'The country converter (coco) - '
        'a Python package for converting country names '
        'between different classifications schemes.'),
    long_description=open('README.rst').read(),
    url='https://github.com/konstantinstadler/country_converter',
    author='Konstantin Stadler',
    author_email='konstantin.stadler@ntnu.no',
    version=__version__,
    packages=['country_converter', ],
    package_data={'country_converter': ['country_data.txt', '../LICENSE']},
    license='GPLv3',
    entry_points={
        'console_scripts':
        ['coco = country_converter.country_converter:main']},
    install_requires=['pandas >= 0.17.0'],
    classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Topic :: Scientific/Engineering',
          'Topic :: Utilities',
          ],
)
