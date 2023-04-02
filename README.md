### A package that can segregate variable names and values from a data file using the info in a seperate excel file

## Installation

Create a [new python environment](https://conda.io/projects/conda/en/latest/user-guide/getting-started.html), if you already don't have one. Make sure `pip` is installed in that environment. You can quickly check that by running the following in a terminal session:

    which pip
    > /Users/gup037/miniconda3/envs/general/bin/pip

If you see something like the above output, you're all set to install this package.<br>
To do that, run this command:

    pip install -U git+https://github.com/vivgastro/field_segregator

If the installation is succesful, then you're in shape to use the package.
Try running the following:

    sep_fields -h

If you see a `usage` and `options` description, then you're all set to use the package

## Usage

Read the output of the `sep_fields -h` carefully. You need to specify the requested options

> -e requires the path to the excel file  
> -s requires the section heading to parse  
> -d requires the path to the data file  
> -o requires the name of the output file (optional)  

An example usage of the script would be:

    sep_fields -e test_data/Data_LayoutPLFS.xlsx -s "PLFS Person Level Data of First Visit Schedule" -d test_data/FPER_FV.10.txt -o ./FPER_FV.10.csv

## Help

If you get stuck anywhere, contact the author [Vivek Gupta](mailto:vivg269@gmail.com)
