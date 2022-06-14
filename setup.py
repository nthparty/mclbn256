from setuptools import setup, Distribution

class BinaryDistribution(Distribution):
	# required for setuptools to autodetect the right naming
	has_ext_modules = lambda _ : True

setup(distclass=BinaryDistribution)
