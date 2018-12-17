from setuptools import setup, find_packages

setup(
    name='skygrid-docker-worker',
    version='0.5.7',
    url='https://github.com/skygrid/docker-worker',
    author='Alexander Baranov',
    author_email='sashab1@yandex-team.ru',
    packages=find_packages(),
    description='SkyGrid docker worker',
    install_requires=[
        "lockfile",
        "requests>=2.5.1",
        "docker",
        #"six",
        "raven",
        "hep-data-backends",
        "marshmallow",
        "protobuf",
        "PyYAML",
        "grpcio",
        "protobuf",
        "numpy"
    ],
    scripts=[
        'scripts/test-descriptor'
    ]
)
