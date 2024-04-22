from os.path import isfile, exists, dirname, join, isdir
from os import getcwd
from glob import glob
from re import findall, escape
from argparse import ArgumentParser
from pydantic import BaseModel
from cli_pprinter import CLIPPrinter
from file_handler import FileHandler
from unidecode import unidecode

PROJECTS_FOLDER = join(dirname(__file__), 'projects_folder.txt')

class CToolStringArgs(BaseModel):
    string:str
    folder_path:str|None
    should_print:bool

class SaveFolderArgs(BaseModel):
    folder_path:str

class Printer:
    def __init__(self, should_print:bool) -> None:
        self.should_print=should_print
        
    def print_red(self, msg:str):
        if self.should_print:
            CLIPPrinter.red(msg, end='')

    def printa(self, msg:str):
        if self.should_print:
            print(msg)

def c_tool_string(string:str, folder_path:str = None, should_print:bool = False, case_sensitive:bool = False, dont_remove_punctuation_accents:bool = False):
    "returns a dictionary with keys as file_paths and value the number of times the string was found in that file"\
    "\n\nif `folder_path` is None, will use current working folder. if `should_print`, will print the results during execution"
    printer = Printer(should_print)
    CToolStringArgs(
        string=string,
        folder_path=folder_path,
        should_print=should_print
    )
    if folder_path is None:
        folder_path = getcwd()
    if not exists(folder_path):
        raise ValueError(f"folder_path {folder_path} doesn't exist!")
    printer.printa(f'\nSEARCHING string {string} in {folder_path}...')
    file_paths = [
        f for f in glob(f'{folder_path}/**/*', recursive=True) if isfile(f) and f[-3:] == '.py'
    ]
    found = {}
    if not dont_remove_punctuation_accents:
        string = unidecode(string)
    if not case_sensitive:
       string = string.lower() 
    for file in file_paths:
        printer.printa(f"Checking file {file}")
        data = FileHandler.load(file_paths=file, load_first_value=True)
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
    printer.printa('_'*100)
    printer.printa(f'\nRESULTS...')
    if not found:
        printer.printa(f"The string {string} wasn't found in any.py file in {folder_path}")
    else:
        total = 0
        for file, count in found.items():
            if count:
                printer.print_red(f'{file}: Found {count} times')
            else:
                printer.printa(f'{file}: NOT FOUND')
            total += count
        printer.printa(f'\nTotal finds: {total}\n')
    return found
    
def save_folder_path(folder_path:str):
    SaveFolderArgs(folder_path=folder_path)
    if not exists(folder_path):
        raise ValueError(f"folder_path {folder_path} doesn't exist!")
    if not isdir(folder_path):
        raise ValueError(f'folder_path {folder_path} is not a directory.')
    FileHandler.write({PROJECTS_FOLDER: folder_path})
    print(f'New folder set: {folder_path}!')

def cli():
    main_path = None
    if exists(PROJECTS_FOLDER):
        main_path = FileHandler.load(file_paths=PROJECTS_FOLDER, load_first_value=True)
    parser = ArgumentParser(description="A script that processes a file.")
    parser.add_argument("string", nargs="?", help="String to search for in files")
    parser.add_argument("-f", action="store_true", help="Path to the folder to search in")
    parser.add_argument("-nf", help="Path to the new_folder to search in")
    parser.add_argument("-cw", action="store_true", help="check in current directory, else check in set folder (-f to see the folder)")
    parser.add_argument('-cs', action="store_true", help='compare string considering case sensitivity')
    parser.add_argument('-drpa', action='store_true', help="don't remove punctuation and accents, so it will consider punctuation and accents when comparing strings")
    args = parser.parse_args()
    if args.f:
        print(f'c_tool_string will search in folder {main_path}!')
    if args.nf:
        main_path = args.nf
        save_folder_path(args.nf)
    if args.cw:
        projeto = getcwd()
    else:
        projeto = main_path
    if args.string:
        if not projeto:
            CLIPPrinter.red('\nno folder was set yet! using current working folder...')
        c_tool_string(
            string=args.string,
            folder_path=projeto,
            should_print=True,
            case_sensitive=args.cs,
            dont_remove_punctuation_accents=args.drpa
        )

if __name__ == '__main__':
    cli()