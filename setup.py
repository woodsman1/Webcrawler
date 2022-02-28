from setuptools import setup, find_packages

print("here")
setup(
  name = 'url-crawler-validation-prediction',
  version='1.0.0',
  description='A simple web crawler, targets link validation test and predict it as harmful or benign',
  author='woodsman',
  author_email='mgoyani78@gmail.com',
  url = 'https://github.com/woodsman1/Webcrawler',
  # license='MIT',
  packages=find_packages(exclude=['tests']),
  install_requires = [
    'lxml',
    'requests',
  ],
  classifiers=[
    'Programming Language :: Python :: 3',
  ],
  entry_points={
    'console_scripts':[
      'webcrawler = crawler:main'
    ]
  }
)