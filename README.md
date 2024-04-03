check for strings in py files in a folder (and subfolder).

## Shell Commands

```bash
# storing a folder (it will be saved and the next commands will search strings in that folder)
c_tool_string -nf folder

# checking what folder is stored
c_tool_string -f

# checking for "oi" string in stored folder
c_tool_string oi

# checking for "oi" string in current folder
c_tool_string oi -cw
```

# Python

```python
from c_tool_string import c_tool_string

# checking for "oi" in folder "folder"
# c_tool_string function has should_print argument. If true, will print the results
c_tool_string(string="oi", folder="folder")
```
