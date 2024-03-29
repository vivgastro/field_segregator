import numpy as np
import argparse
import pandas as pd
import tqdm


def segregate_fields(inp_file, out_file, field_names, byte_starts, byte_ends):
    '''
    Segregates the fields based on the field byte_start and byte_end values
    Reads in the data row by row from 'inp_file' and writes the segregated
    output to 'out_file'.

    Params
    ------
    inp_file: str
            Path to the data file
    out_file: str
            Path to the output data file after segregation
    field_names: list
            A list of strings, which contain the field/variable names
    byte_starts: list
            A list of integers, which indicate the starting byte (1-indexed, inclusive range)
            of the values in each row
    byte_ends: list
            A list of integers, which indicate the end byte (1-indexed, inclusive range)
            of the values in each row
    '''

    #Open the input file and read all the lines as string
    with open(inp_file) as f:
        lines = f.readlines()

    #If outname is not provided, generate a default one by changing the extension to .csv
    if out_file is None:
        out_file = inp_file.strip(".txt") + ".csv"

    #Open the out_file in 'write' mode
    o = open(out_file, 'w')

    ncols = len(field_names)
    
    #Write out the field_names/keys/variables first as column headers
    for icol in range(ncols):
        o.write(field_names[icol] + ",")
    o.write("\n")

    print("Now segregating the data fields line by line....")
    #Now loop over the data file line by line and split the values using the parsed info
    for ii, line in enumerate(tqdm.tqdm(lines)):
        #print(ii)
        oline = ""
        for icol in range(ncols):
            key = field_names[icol]
            #print(f"key = {key}, byte_start = {byte_starts[icol]}, byte_ends = {byte_ends[icol]}")
            value = line[int(byte_starts[icol]) - 1 : int(byte_ends[icol])]     #byte_starts and byte_ends are 1-indexed inclusive-range endpoint markers
            oline += value
            oline += ","
        o.write(oline.strip(",") + "\n")        #Get rid of the last comma, and put a new-line instead


def parse_excel_file(fname, header):
    '''
    Parses the excel file and looks for the desired section. It returns a list of
    variable names (keys) and the byte_starts, byte_ends of the values.

    Params
    ------
    fname: str
            Path to the excel file which contains the variable info
    header: str
            The name of the section which has to be parsed
            It is case-sensitive

    Returns
    -------
    field_names: list
            A list of strings, which contain the field/variable names
    byte_starts: list
            A list of integers, which indicate the starting byte (1-indexed, inclusive range)
            of the values in each row
    byte_ends: list
            A list of integers, which indicate the end byte (1-indexed, inclusive range)
            of the values in each row


    '''

    print(f"Parsing variable information from excel file - {fname}")
    f = pd.read_excel(fname)
    nrows = len(f)
    irow = -1
    section_start = -1
    section_end = -1
    field_names = []
    byte_starts = []
    byte_ends = []
    while True:
        irow +=1
        row = f.iloc[irow]
        if row[0] == header:
            #Target section found, update the section start value and go to the next line
            print("Found the section at row number - ", irow)
            section_start = irow
            continue

        if section_start > -1 and section_end == -1:
            #This line is within the target section... read the values and go to next line
            #print("Extracting info from row - ", row)
            field_name = row[1]
            byte_start = row[5]
            byte_end = row[6]

            field_names.append(field_name)
            byte_starts.append(byte_start)
            byte_ends.append(byte_end)

        if section_start > -1 and type(row[0]) == float and np.isnan(row[0]):
            #We have reached the end of the section
            section_end = irow-1
            print("Finished scanning the desired section")
            break
        if section_end == -1 and irow >= nrows:
            print(f"Could not find the section {header} in the file {fname}!")
            sys.exit(1)

    return field_names[1:-1], byte_starts[1:-1], byte_ends[1:-1]


def get_parser():
    a = argparse.ArgumentParser()
    a.add_argument("-e", dest="excel_file", type=str, help="Path to the excel file containing the field info", required = True)
    a.add_argument("-s", dest="section", type=str, help="Section Heading which needs to be extracted", required = True)
    a.add_argument("-d", dest="datafile", type=str, help="Path to the data file which contains the values", required = True)
    a.add_argument("-o", dest="outfile", type=str, help="Path to the output file name (optional; default=excel_file.csv)", default=None)

    args = a.parse_args()
    return args


def main():
    args = get_parser()
    a, b, c  = parse_excel_file(args.excel_file, args.section.strip())
    segregate_fields(args.datafile, args.outfile, a[1:], b[1:], c[1:])

if __name__ == '__main__':
    main()
