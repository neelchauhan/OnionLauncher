#!/usr/bin/env python

from setuptools import setup
import sys

setup(name="OnionLauncher",
	version="0.0.1",
	description="Launcher for Tor",
	license = "BSD",
	author="Neel Chauhan",
	author_email="neel@neelc.org",
	url="https://www.github.com/neelchauhan/OnionLauncher/",
	packages=["OnionLauncher"],
	entry_points={'gui_scripts': ['OnionLauncher=OnionLauncher.main:main_loop']},
	package_data={"OnionLauncher": ["ui_files/*"]},
	install_requires=[
		"stem",
	],
	data_files=[
		(sys.prefix + "/share/pixmaps", ["icons/scalable/onionlauncher.svg"]),
		(sys.prefix + "/share/applications", ["data/onionlauncher.desktop"]),
	],
	classifiers=[
		"Environment :: X11 Applications :: Qt",
		"Intended Audience :: End Users/Desktop",
		"License :: OSI Approved :: BSD License",
		"Programming Language :: Python :: 2",
		"Programming Language :: Python :: 3",
	],
)
