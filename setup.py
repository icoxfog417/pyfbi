import os
from setuptools import setup


requires = ["tornado>=4.5.2"]


def get_statics(folders):
    static_files = []
    root = "pyfbi/visualize/"
    targets = [root + f for f in folders]
    for (path, dir, filenames) in os.walk(root):
        for t in targets:
            if t in path:
                if len(filenames) > 0:
                    for f in filenames:
                        f = os.path.join(path, f).replace(root, "")
                        static_files.append(f)
                continue
    
    return static_files


setup(
    name="pyfbi",
    version="0.2.0",
    description="pyFBI enables 'as much as needed' profiling by decorator",
    url="https://github.com/icoxfog417/pyfbi",
    author="icoxfog417",
    author_email="icoxfog417@yahoo.co.jp",
    license="MIT",
    keywords="performance-analysis pstat profile",
    packages=[
        "pyfbi",
        "pyfbi.visualize",
    ],
    package_data={
        "pyfbi.visualize": get_statics(["static", "templates"])
    },
    entry_points={
        "console_scripts": ["pyfbi_viz=pyfbi.pyfbi_viz:main"],
    },
    install_requires=requires,
    classifiers=[
        "Programming Language :: Python :: 3.6",
    ],
)
