from setuptools import setup

setup(name='parse_doi',
      version='0.1',
      packages=['parse_doi'],
      url='',
      license='MIT',
      install_requires=[
           'tqdm', 'pandas', 'crossrefapi', 'pyscopus', 'requests_html'
      ],
      extras_require={
          'testing': ['pytest', 'pytest-cov<2.6'],
          'docs': ['sphinx-rtd-theme', 'sphinxcontrib-bibtex'],
          'pre-commit': [
              'pre-commit==1.11.0', 'yapf==0.24.0', 'prospector==1.1.5',
              'pylint==1.9.3'
          ]
      },
      author='Kevin M. Jablonka',
      author_email='kevin.jablonka@epfl.ch',
      classifiers=[
          "Programming Language :: Python :: 3.6",
          "Development Status :: 1 - Beta",
          "Intended Audience :: Science/Research",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
          "Topic :: Scientific/Engineering :: Physics",
          "Topic :: Scientific/Engineering :: Chemistry",
          "Topic :: Software Development :: Libraries :: Python Modules"
      ],
      description='tool to parse full texts of papers given a dictionary of regexes and DOIs')
