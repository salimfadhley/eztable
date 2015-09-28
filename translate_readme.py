from pypandoc import convert

def convert_readme_files():
    with open("readme.md", encoding='utf-8') as input_file, open("src/readme.rst", "w") as output_file:
        input_string = input_file.read()
        converted = convert(input_string, 'rst', format="md")
        output_file.write(converted)

if __name__ == '__main__':
    convert_readme_files()