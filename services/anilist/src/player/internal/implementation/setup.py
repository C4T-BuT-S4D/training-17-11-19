from distutils.core import setup, Extension

aniparser_module = Extension('aniparser', sources=['aniparser.c'])

setup(name='aniparser',
      version='1.0',
      description='aniparser module',
      ext_modules=[aniparser_module])
