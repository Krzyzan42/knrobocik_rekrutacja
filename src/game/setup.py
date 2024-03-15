from glob import glob
import os
from setuptools import find_packages, setup

package_name = 'game'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='krzyzan',
    maintainer_email='jakubkrzyzanowski42@gmail.com',
    description='Zadanie rekrutacyjne dla knRobocik',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'board = game.board:main',
            'controller = game.controller:main'
        ],
    },
)
