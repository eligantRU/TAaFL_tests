# Conversion auto-tests
> python test_conversion.py <PROGRAM_PATH>

## Limitations
It correctly works only if your program works with stdin/stdout or take two command line arguments(input & output file paths).

>Do not mix both these options!

In your output u can use any characters: this tool checks numbers only.

## Tests set
U can expand tests set by this way:
1) Create new folder(folder name shows as a test-case name)
2) Add your input file as "input.txt"
3) Add your expected output as "expected_output.txt"
4) Add your expected Graphiz formatted graph as "expected_graph.dot"

## Supports extensions:
* `.exe`
* `.py`
* `.jar` (maybe)

### Examples:
> python test_conversion.py AutomataConverter.exe

> python test_conversion.py ../AutomataConverter.exe

> python test_conversion.py AutomataConverter.py
