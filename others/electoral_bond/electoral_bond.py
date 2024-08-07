import PyPDF2
import pandas as pd
import re

def get_first_int_character_position(s):
    for i, char in enumerate(s):
        if char.isdigit():
            return i
    return -1  # Return -1 if no integer character is found

def separate_amount_from_name(string):
    # Start from the end of the string
    index = len(string) - 1
    amount = ""

    # Find the first space going backwards
    while index >= 0 and string[index] != ' ':
        # Ignore commas
        if string[index] != ',':
            amount = string[index] + amount
        index -= 1

    # After finding the space, the remaining part is the name
    name = string[:index].strip()

    return name, amount


def parse_line(line):
    # Define regular expressions for the patterns
    pattern1 = r'^.{1,11}'
    pattern2 = r'(\d.*)'
    pattern3 = r'(?<=\d)[^\d]*$'

    # Apply regular expressions to split the string
    part1 = line[:11]
    rest = line[11:]
    name, amount = separate_amount_from_name(rest)
    
    return part1, name, amount

def extract_table_from_pdf(pdf_path, start_page, end_page):
    table_data = []

    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        for page in pdf_reader.pages:

            text = page.extract_text()
            
            # Split text into lines and extract table-like data
            lines = text.split('\n')
            for line in lines:
                if len(line) >= 6:  # Assuming at least 6 characters for each line
                    table_data.append(parse_line(line))
            
    return table_data

def save_to_excel(table_data, output_path):
    df = pd.DataFrame(table_data, columns=['Column1', 'Column2', 'Column3'])
    df.to_excel(output_path, index=False)

def convert_pdf_to_excel(pdf_path, start_page, end_page, output_path):
    table_data = extract_table_from_pdf(pdf_path, start_page, end_page)
    save_to_excel(table_data, output_path)

# Example usage
pdf_path = 'bonds.pdf'  # Path to your PDF file
start_page = 1  # Start page of the table
end_page = 3  # End page of the table
output_path = 'bond-part1.xlsx'  # Path where the Excel file will be saved

convert_pdf_to_excel(pdf_path, start_page, end_page, output_path)
