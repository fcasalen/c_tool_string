from os.path import isfile, exists
from os import getcwd
from glob import glob
from re import findall, escape
from argparse import ArgumentParser
from pydantic import BaseModel
from cli_pprinter import CLIPPrinter
from file_handler import FileHandler
from unidecode import unidecode
from tqdm import tqdm

class CToolStringArgs(BaseModel):
    string:str
    folder_path:str|None

def c_tool_string(string:str, folder_path:str = None, case_sensitive:bool = False, dont_remove_punctuation_accents:bool = False):
    "returns a dictionary with keys as file_paths and value the number of times the string was found in that file"\
    "\n\nif `folder_path` is None, will use current working folder."
    CToolStringArgs(
        string=string,
        folder_path=folder_path,
    )
    if folder_path is None:
        folder_path = getcwd()
    if not exists(folder_path):
        raise ValueError(f"folder_path {folder_path} doesn't exist!")
    CLIPPrinter.green(f'\nSEARCHING string {string} in {folder_path}...')
    file_paths = [
        f for f in glob(f'{folder_path}/**/*', recursive=True) if isfile(f) and f[-3:] == '.py'
    ]
    files = {}
    if not dont_remove_punctuation_accents:
        string = unidecode(string)
    if not case_sensitive:
       string = string.lower()
    total = 0
    for file in tqdm(file_paths, desc='Files assessed', unit='file'):
        data = FileHandler.load(file_paths=file, load_first_value=True, progress_bar=False)
        if not dont_remove_punctuation_accents:
            data = unidecode(data)
        if not case_sensitive:
            data = data.lower()
        count = len(findall(
            pattern = escape(string),
            string = data
        ))
        files[file] = 0
        if count:
            files[file] = count
            total += count
    print()
    CLIPPrinter.white(f'{"*"*46}RESULTS{"*"*46}')
    CLIPPrinter.white_underline(f'Count of {string} found in each file:')
    found = []
    for file, count in files.items():
        if count:
            found.append(f'{file}: Found {count} times')
            CLIPPrinter.red(f'{file}: Found {count} times', end='')
        else:
            print(f'{file}: NOT FOUND')
    print()
    CLIPPrinter.line_breaker('-')
    CLIPPrinter.white_underline(f'Total finds: {total}:')
    CLIPPrinter.red(f"\n".join(found))
    CLIPPrinter.line_breaker()
    return files

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
        case_sensitive=args.cs,
        dont_remove_punctuation_accents=args.drpa
    )

if __name__ == '__main__':
    cli()