from setuptools import setup


requirements = ['numpy', 'pandas', 'tqdm', 'argparse']

setup(name="field_segregator", 
      version=0.1,
      description="A module to seperate the fields from a text file",
      author="Vivek Gupta",
      author_email="vivg269@gmail.com",
      install_requires=requirements,
      python_requires='>=3.6',
      packages=['field_segregator'],
      entry_points={'console_scripts':['sep_fields=field_segregator.segregate_fields_from_text_file:main']}
      )

