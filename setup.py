import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name='flask_request',
    version='0.0.1',
    author='David Beahm',
    author_email='Beahmer89@gmail.com',
    license='BSD',
    description='Flask Extension for external requests',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Beahmer89/flask-request",
    packages=setuptools.find_packages(),
    install_requires=['requests'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    python_requires='>=3.6',
)
