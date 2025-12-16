from argparse import ArgumentParser
from pathlib import Path
from re import escape, findall

from tqdm import tqdm
from unidecode import unidecode


def c_tool_string(
    string: str,
    encoding: str = "utf-8",
    folder_path: str = None,
    case_sensitive: bool = False,
    dont_remove_punctuation_accents_marks: bool = False,
):
    """returns a dictionary with keys as file_paths and value the number of
    times the string was found in that file.

    if `folder_path` is None, will use current working folder.

    Args:
        string (str): string to search for in files
        encoding (str, optional): encoding to open files. Defaults to "utf-8".
        folder_path (str, optional): path to folder to search in. Defaults to None
            (uses current working directory).
        case_sensitive (bool, optional): whether to consider case sensitivity when
            comparing strings.
            Defaults to False.
        dont_remove_punctuation_accents_marks (bool, optional): whether to consider
            punctuation and accents when comparing strings. Defaults to False.

    Raises:
        ValueError: if folder_path doesn't exist
        AssertionError: if string is not a str or folder_path is not a str or None

    Returns:
        dict: keys are file paths and values are the number of times the string
            was found in that file
    """
    assert isinstance(string, str), "string must be a str"
    assert folder_path is None or isinstance(folder_path, str), (
        "folder_path must be a str or None"
    )
    folder_path: Path = Path(folder_path) if folder_path else Path.cwd()
    if not folder_path.exists():
        raise ValueError(f"folder_path {folder_path} doesn't exist!")
    print("-" * 100)
    print(f"SEARCHING string {string} in {folder_path}...")
    file_paths = [f for f in folder_path.rglob("*.py") if f.is_file()]
    files = {}
    if not dont_remove_punctuation_accents_marks:
        string = unidecode(string)
    if not case_sensitive:
        string = string.lower()
    total = 0
    for file in tqdm(file_paths, desc="Files assessed", unit="file"):
        with open(file, "r", encoding=encoding) as f:
            data = f.read()
        if not dont_remove_punctuation_accents_marks:
            data = unidecode(data)
        if not case_sensitive:
            data = data.lower()
        count = len(findall(pattern=escape(string), string=data))
        files[str(file)] = 0
        if count:
            files[str(file)] = count
            total += count
    print(f"\n{'*' * 46}RESULTS{'*' * 46}")
    print(f"Count of {string} found in each file:")
    found = []
    for file, count in files.items():
        if count:
            found.append(f"{file}: Found {count} times")
            print(f"{file}: Found {count} times", end="")
        else:
            print(f"{file}: NOT FOUND")
    print()
    print("-" * 100)
    print(f"\nTotal finds: {total}:")
    print("\n".join(found))
    print("-" * 100)
    return files


def cli():
    parser = ArgumentParser(
        description="A script that search strings in py files ina given folder"
    )
    parser.add_argument("string", help="String to search for in files")
    parser.add_argument(
        "-f",
        help="Path to the folder to search in. Default to current directory if not "
        "passed",
    )
    parser.add_argument(
        "-cs", action="store_true", help="compare string considering case sensitivity"
    )
    parser.add_argument(
        "-drpa",
        action="store_true",
        help="don't remove punctuation and accents marks, so it will consider "
        "punctuation and accents marks when comparing strings",
    )
    args = parser.parse_args()
    c_tool_string(
        string=args.string,
        folder_path=args.f,
        case_sensitive=args.cs,
        dont_remove_punctuation_accents_marks=args.drpa,
    )


if __name__ == "__main__":
    cli()
