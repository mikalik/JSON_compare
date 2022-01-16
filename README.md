Description
===
Python file `json_compare` is simple util for camparison of 2 JSON files. Certainly, the file may be used like module for Yours program, because it make difference by initialize object `Diff()` with logging of difference `instance.logging_analysis` in pyton dictionary.
```python
def __init__(self, first: dict or list, second: dict or list, print_param=False, paths=''):
        self.logging_analysis = {'PATH': {}, 'TYPE': {}, 'VALUE': {}, 'INDEX_ERROR': {}, 'FILES': paths}
```

Using
---
```bash
python3 json_compare.py <path1> <path2> <parameter of output>
```
_parameter of output_:
- `-s` -- only screen output **(default value)**
- `-f` -- only file **(result.json)** output
- `-fs` or `-sf` -- screen and file output

# Example
For screen
---
```bash
-------1st file-------
FOR ~DIFF VALUES~
1st | 2nd file @PATH

FOR ~NEED TO CUT~
ITEM (for cut) @PATH
----------------------
-       JSON HAVE ADDITIONAL ELEM
 first_name
+-      VALUE DIFFERS
 False | True @isAlive
-       JSON HAVE ADDITIONAL ELEM
 Age
?       DIFFERENT TYPE OF VALUE
 str | int @address/stress[0]
+-      VALUE DIFFERS
 Chicago | New York @address/city
+-      VALUE DIFFERS
 IL | NY @address/state
-------2nd file-------
-       JSON HAVE ADDITIONAL ELEM
 firstName
-       JSON HAVE ADDITIONAL ELEM
 age
!       NEED TO CUT
 2 @address/stress[1]
-       JSON HAVE ADDITIONAL ELEM
 address/postalCode
```
For file (`int` of value for keys are ordinal number of JSON-files in CLI)   
---
```json
{"PATH": {"first_name": 1, "Age": 1, "firstName": 2, "age": 2, "address/postalCode": 2}, "TYPE": {"str | int @address/stress[0]": 1}, "VALUE": {"False | True @isAlive": 1, "Chicago | New York @address/city": 1, "IL | NY @address/state": 1}, "INDEX_ERROR": {"2 @address/stress[1]": 2}, "FILES": ["sys.json", "sys2.json"]}
```