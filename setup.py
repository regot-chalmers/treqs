from setuptools import setup

setup(name='treqs',
      version='0.1',
      description='Tool Support for Managing Requirements in Large-Scale Agile System Development',
      url='https://github.com/regot-chalmers/treqs',
      author='Eric Knauss',
      author_email='eric.knauss@cse.gu.se',
      license='MIT',
      packages=['treqs'],
      scripts=['bin/treqs'],
      zip_safe=False)
