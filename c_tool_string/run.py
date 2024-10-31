from os.path import isfile, exists
from os import getcwd
from glob import glob
from re import findall, escape
from argparse import ArgumentParser
from pydantic import BaseModel
from cli_pprinter import CLIPPrinter
from file_handler import FileHandler
from unidecode import unidecode

class CToolStringArgs(BaseModel):
    string:str
    folder_path:str|None
    should_print:bool

class SaveFolderArgs(BaseModel):
    folder_path:str

def c_tool_string(string:str, folder_path:str = None, should_print:bool = False, case_sensitive:bool = False, dont_remove_punctuation_accents:bool = False):
    "returns a dictionary with keys as file_paths and value the number of times the string was found in that file"\
    "\n\nif `folder_path` is None, will use current working folder. if `should_print`, will print the results during execution"
    CToolStringArgs(
        string=string,
        folder_path=folder_path,
        should_print=should_print
    )
    if folder_path is None:
        folder_path = getcwd()
    if not exists(folder_path):
        raise ValueError(f"folder_path {folder_path} doesn't exist!")
    CLIPPrinter.white(f'\nSEARCHING string {string} in {folder_path}...')
    file_paths = [
        f for f in glob(f'{folder_path}/**/*', recursive=True) if isfile(f) and f[-3:] == '.py'
    ]
    found = {}
    if not dont_remove_punctuation_accents:
        string = unidecode(string)
    if not case_sensitive:
       string = string.lower() 
    for file in file_paths:
        print(f"Checking file {file}")
        data = FileHandler.load(file_paths=file, load_first_value=True, progress_bar=False)
        if not dont_remove_punctuation_accents:
            data = unidecode(data)
        if not case_sensitive:
            data = data.lower()
        count = len(findall(
            pattern = escape(string),
            string = data
        ))
        found[file] = 0
        if count:
            found[file] = count
    CLIPPrinter.white(f'\nRESULTS')
    if not found:
        CLIPPrinter.yellow(f"The string {string} wasn't found in any.py file in {folder_path}")
    else:
        total = 0
        for file, count in found.items():
            if count:
                CLIPPrinter.red(f'{file}: Found {count} times', end='')
            else:
                print(f'{file}: NOT FOUND')
            total += count
        CLIPPrinter.white_underline(f'\nTotal finds: {total}\n')
    return found

def cli():
    parser = ArgumentParser(description="A script that search strings in py files ina given folder")
    parser.add_argument("string", help="String to search for in files")
    parser.add_argument("-f", help="Path to the folder to search in. Default to current directory if not passed")
    parser.add_argument('-cs', action="store_true", help='compare string considering case sensitivity')
    parser.add_argument('-drpa', action='store_true', help="don't remove punctuation and accents, so it will consider punctuation and accents when comparing strings")
    args = parser.parse_args()
    c_tool_string(
        string=args.string,
        folder_path=args.f,
        should_print=True,
        case_sensitive=args.cs,
        dont_remove_punctuation_accents=args.drpa
    )

if __name__ == '__main__':
    cli()