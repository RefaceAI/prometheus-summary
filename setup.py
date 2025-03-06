import pathlib
import setuptools
from importlib.machinery import SourceFileLoader

version = SourceFileLoader("version", "prometheus_summary/version.py").load_module()


def readfile(filename) -> str:
    return pathlib.Path(filename).read_text("utf-8").strip()


setuptools.setup(
    name="prometheus-summary",
    version=version.__version__,
    author="RefaceAI",
    author_email="github-support@reface.ai",
    description="Prometheus summary with quantiles over configurable sliding time window",
    long_description=readfile("README.md"),
    long_description_content_type="text/markdown",
    license="Apache License 2.0",
    url="https://github.com/RefaceAI/prometheus-summary",
    packages=["prometheus_summary"],
    install_requires=[
        "prometheus_client>=0.11.0",
        "quantile-estimator>=0.1.0",
    ],
    platforms="Platform Independent",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
)
