from distutils.core import setup
setup(
    name='valvepcf',
    packages=['valvepcf'],
    version='1.1.0',
    license='gpl-3.0',
    description='A library to parse .pcf files used by the source engine.',
    author='Maxime Dupuis',
    author_email='mdupuis@hotmail.ca',
    url='https://github.com/pySourceSDK/ValvePCF',
    download_url='https://github.com/pySourceSDK/ValvePCF/archive/v1.1.0.tar.gz',
    keywords=['pcf', 'source', 'sourcesdk', 'hammer', 'valve'],
    install_requires=['construct', 'future'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
)
