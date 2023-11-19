from setuptools import setup, find_packages

setup(
    name='intgcal',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        icalendar,
        pytz,
        pytest,
    ],
    entry_points={
        'console_scripts': [
            'your_tool_name=src.main:main',  # Replace 'your_tool_name' and 'src.main:main' appropriately
        ],
    },
)
