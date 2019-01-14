from setuptools import setup, find_packages

setup(
    name="vis-gpu-usage",
    version="1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Click",
        "matplotlib",
    ],
    entry_points='''
        [console_scripts]
        vis_gpu_usage=vis_gpu_usage:cli
    ''',
)
