from setuptools import setup, find_packages

package_name = "tera_crystal_ball"
package_version = "1.0.0"
description = """OpenAI"""

setup(
    name=package_name,
    version=package_version,
    author="Teradata Corporation",
    description=description,
    packages=find_packages(),
    install_requires=[
        'python-dotenv',
        'openai',
        'teradatasql>=16.20.0.0',
        'pytest~=7.0'
    ],
    python_requires=">=3.8,<3.12",
)
