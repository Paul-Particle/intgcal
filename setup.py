from setuptools import setup, find_packages

setup(
    name='intgcal',
    version='0.2.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=[
        'icalendar',
        'pytz',
        'pytest',
    ],
    entry_points={
        'console_scripts': [
            'intgcal=intgcal.main:cli_wrapper',
        ],
    },
)
