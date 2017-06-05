from setuptools import setup

setup(name='Mnist Digit Sequence Generator',
      version='1.0',
      description='Generate images of digit sequences from MNIST data.',
      author='Evan Sparks',
      author_email='evan.c.sparks@gmail.com',
      packages=['sequencegen'],
      install_requires=['numpy', 'pypng']
      )
