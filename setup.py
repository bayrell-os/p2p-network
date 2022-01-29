#!/usr/bin/env python3
# -*- coding: utf-8 -*- 


"""
Инструкции:

python3 setup.py sdist bdist_wheel - Сборка пакета
sudo python3 setup.py develop - Установка пакета для разработки
sudo python3 setup.py develop -u - Uninstall
sudo pip3 install dist/game_network-0.1.tar.gz - Установка пакета
sudo pip3 uninstall game_network - Удаление пакета
python3 -m twine upload --repository pypi dist/* - Залить на сервер
twine upload -r pypi dist/* - Новая команда залить в pypi

Список классификации:
https://pypi.python.org/pypi?%3Aaction=list_classifiers
"""


from setuptools import setup, find_packages
from os.path import abspath, dirname, join

setup(
	name="game_network",
	version="0.1",
	description="P2P Game Network",
	long_description=open(join(abspath(dirname(__file__)), 'README.md'), encoding='utf-8').read(),
	long_description_content_type='text/markdown',
	license="GPL-3.0 License",
	url = "https://github.com/bayrell-os/p2p-network",
	packages=find_packages(),
	include_package_data = True,
	scripts=[
		'scripts/game_network'
	],
	install_requires=[
		'PyQt5',
		'PyQtWebEngine',
	],
	classifiers=[
		'Environment :: X11 Applications :: Qt',
		'License :: OSI Approved :: Apache Software License',
		'Operating System :: POSIX :: Linux',
		'Operating System :: Microsoft :: Windows :: Windows 10',
		'Programming Language :: Python',
		'Programming Language :: Python :: 3',
		'Topic :: Internet',
		'Topic :: System :: Operating System',
		'Topic :: Utilities',
	],
	keywords = [
		"game network", "peervpn"
	],
)