try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'skeleton test',
    'author': 'Maurice',
    # 'url': 'URL to get it at.',
    # 'download_url': 'Where to download it.',
    'author_email': 'maurice.jarck@email.com',
    'version': '0.1',
    # 'install_requires': ['nose'],
    # 'packages': ['NAME'],
    # 'scripts': [],
    'name': 'test_skeleton'
}

setup(**config)
