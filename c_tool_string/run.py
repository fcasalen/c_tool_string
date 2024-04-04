from os.path import isfile, exists, dirname, join
from os import getcwd
from glob import glob
from re import findall, escape
from argparse import ArgumentParser
from pydantic import BaseModel
from cli_pprinter import CLIPPrinter

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
            CLIPPrinter.red(msg)

    def printa(self, msg:str):
        if self.should_print:
            print(msg)

def c_tool_string(string:str, folder_path:str = None, should_print:bool = False):
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
    for file in file_paths:
        printer.printa(f"Checking file {file}")
        with open(file, 'r', encoding = 'utf-8') as f:
            data = f.read()
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
    folder_path = dirname(folder_path)
    with open(PROJECTS_FOLDER, 'w', encoding='utf-8') as f:
        f.write(folder_path)
    print(f'New folder set: {folder_path}!')

def cli():
    main_path = None
    if exists(PROJECTS_FOLDER):
        with open(PROJECTS_FOLDER, 'r', encoding='utf-8') as f:
            main_path = f.read() 
    parser = ArgumentParser(description="A script that processes a file.")
    parser.add_argument("string", nargs="?", help="String to search for in files")
    parser.add_argument("--folder", "-f", action="store_true", help="Path to the folder to search in")
    parser.add_argument("--new_folder", "-nf", help="Path to the new_folder to search in")
    parser.add_argument("--check_cw", "-cw", action="store_true", help="check in current directory, else check in set folder (-f to see the folder)")
    args = parser.parse_args()
    if args.folder:
        print(f'c_tool_string will search in folder {main_path}!')
    if args.new_folder:
        main_path = args.new_folder
        save_folder_path(args.new_folder)
    if args.check_cw:
        projeto = getcwd()
    else:
        projeto = main_path
    if args.string:
        if not projeto:
            print('no folder was set yet! using current working folder...')
        else:
            c_tool_string(
                string=args.string,
                folder_path=projeto,
                should_print=True
            )

if __name__ == '__main__':
    cli()