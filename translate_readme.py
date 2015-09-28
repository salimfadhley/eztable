from pypandoc import convert

def convert_readme_files():
    with open("readme.md", encoding='utf-8') as input_file, open("src/readme.rst", "w") as output_file:
        output_file.write(convert(input_file, 'rst'))

if __name__ == '__main__':
    convert_readme_files()