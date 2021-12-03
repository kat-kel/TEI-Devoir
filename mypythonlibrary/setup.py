from setuptools import find_packages, setup

setup(
	name='mylibrary', # nom de la bibliothèque qui sera appellée dans une fonction
	packages=find_packages(include=['mylibrary']), # préciser quels paquets seront inclus
	version='0.1.0',
	description='My first Python library',
	author='Kelly Christensen',
	licence='ENC',
	# au lieu d'un fichier requirements.txt, le paquet pip 'setuptools' précise des dépendances avec les arguments 'install_requires' et 'tests_require'
	install_requires=[ # précise les paquets obligatoires
		
		],
	setup_requires=['pytest-runner'], # précise le paquet exigé pour tester le code avec la commande 'python setup.py pytest'
	tests_require=['pytest==4.4.1'],
	test_suite='tests', # le valeur 'tests' précise où se trouve le programme demarré par la commande 'python setup.py pytest'
)
