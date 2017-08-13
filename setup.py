from setuptools import setup, find_packages

setup(name="speedtest_sendtest",
      version="0.1",
      description="bash and python scripts to test speed with speedtest-cli and text you the average",
      url="https://github.com/Awesomecase/Speedtest",
      author="Cole Swingholm",
      author_email="cole.swingholm@gmail.com",
      license="GGPL3",
      packages=find_packages(where="src"),
      package_dir={"": "src"},
      zip_safe=False,
      install_requires=["requests"],
      scripts=["bin/speedtest_log"])
