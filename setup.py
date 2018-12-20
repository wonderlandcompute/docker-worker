from setuptools import setup, find_packages

setup(
    name='skygrid-docker-worker',
    version='0.7.0',
    url='https://github.com/wonderlandcompute/docker-worker',
    author='Alexander Baranov && Musinov Igor',
    author_email='sashab1@yandex-team.ru',
    packages=find_packages(),
    description='SkyGrid docker worker',
    install_requires=[
        "lockfile",
        "requests>=2.5.1",
        "docker",
        "raven",
        "hep-data-backends",
        "marshmallow",
        "protobuf",
        "PyYAML",
        "grpcio",
        "numpy"
    ],
    scripts=[
        'scripts/test-descriptor'
    ]
)
