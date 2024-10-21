from distutils.core import setup
setup(
  name = 'bluetermgen',
  packages = ['bluetermgen'],
  version = '0.1',
  license='MIT',
  description = 'Easily create messages, menus or directly visualize table data into the terminal',
  author = 'Nayden Petrov',
  author_email = 'nedd.petrov@gmail.com',
  url = 'https://github.com/DKNorad/blue-terminal-generator',
  download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',
  keywords = ['SOME', 'MEANINGFULL', 'KEYWORDS'],
  install_requires=[
          'validators',
          'beautifulsoup4',
      ],
  classifiers=[
    'Development Status :: 5 - Production/Stable',

    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',

    'License :: OSI Approved :: MIT License',

    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
  ],
)