import json
import sys

PATH = ('-\tJSON HAVE ADDITIONAL ELEM\n', 'PATH')
INDEX = ('!\tNEED TO CUT\n', 'INDEX_ERROR')
TYPE = ('?\tDIFFERENT TYPE OF VALUE\n', 'TYPE')
VALUE = ('+-\tVALUE DIFFERS\n', 'VALUE')

class Differ():
    """Obect of JSON difference
    print_param is parameter of results screen output
    path is note of file difference"""

    def __init__(self, first: dict or list, second: dict or list, print_param=False, paths=''):
        self.logging_analysis = {'PATH': {}, 'TYPE': {}, 'VALUE': {}, 'INDEX_ERROR': {}, 'FILES': paths}
        if print_param:
            print('\n-------1st file-------\nFOR ~DIFF VALUES~\n1st | 2nd file @PATH\n')
            print('FOR ~NEED TO CUT~\nITEM (for cut) @PATH\n----------------------')
            self.analysis(first, second, print_res=True)
            print('-------2nd file-------')
            self.analysis(second, first, print_res=True, iteration=2)
        else:
            self.analysis(first, second)
            self.analysis(second, first, iteration=2)

    def analysis(self, first, second, print_res=False, iteration=1, path='') -> None:
        """Check type of element in subJSON object"""

        if isinstance(first, dict):
            # if len(first):
                for key in first:
                    if len(path) == 0:
                        new_path = key
                    else:
                        new_path = f'{path}/{key}'

                    if isinstance(second, dict):
                        if key in second:
                            self.analysis(first[key], second[key], print_res=print_res, iteration=iteration, path=new_path)
                        else: 
                            self.logging_n_print(PATH, new_path, iteration, print_res)         
                    else:                                               
                        self.checkTypeDiff_n_compare(first, second, iteration, path, print_res)
                        break
            else:
                self.checkTypeDiff_n_compare(first, second, iteration, path, print_res)

        elif isinstance(first, list) and isinstance(second, list):
            for (index, item) in enumerate(first):
                new_path = f'{path}[{index}]'
                match = None                                     
                if second != None:
                    try:
                        match = second[index]
                    except (TypeError, KeyError):                           
                        self.logging_n_print(TYPE, f'{item} @{new_path}', iteration, print_res)
                        break
                    except (IndexError):
                        self.logging_n_print(INDEX, f'{item} @{new_path}', iteration, print_res)
                        break
                
                self.analysis(first[index], match, print_res=print_res, iteration=iteration, path=new_path)

        else:
            self.checkTypeDiff_n_compare(first, second, iteration, path, print_res)

        return None

    def checkTypeDiff_n_compare(self, first, second, iteration: int, path: str, print_res: bool) -> None:
        """Check and compare nesting depth last elements"""

        if type(first) is not type(second) and iteration == 1:
            return self.logging_n_print(TYPE, f'{type(first).__name__} | {type(second).__name__} @{path}', iteration, print_res)                                         
        elif first != second and iteration == 1:
            return self.logging_n_print(VALUE, f'{first} | {second} @{path}', iteration, print_res)
        else:
            return None

    def logging_n_print(self, message_type: set, diff_message: str, iteration: int, print_res: bool) -> None:
        """Save result in field of instance class and print result(optional, default - False)"""

        self.logging_analysis[message_type[1]] [diff_message] = iteration
        if print_res:
            print(message_type[0], diff_message)

        return None


def prepareJsonFile(file_path: str) -> object:
    """Read and deserialize JSON-file"""

    with open (file_path, 'r') as file:
        py_dict = json.load(file)
    return py_dict

def compare_n_output(path_to_1st: str, path_to_2nd: str, compare_param='-s') -> None:
    """Identity of nested objects check and filling comparison 2 JSON files, 
    initsialize object of JSON differens.
    "compare_param" is the parameter of output:  '-f' - only file, '-sf' or '-fs' - screen and file, default - only screen"""

    json_1st = prepareJsonFile(path_to_1st)
    json_2nd = prepareJsonFile(path_to_2nd)
    paths = [path_to_1st, path_to_2nd]
    if type(json_1st) is not type(json_2nd):
        print(f'Different objects in JSON files:                \
            \n1st file: {(type(json_1st).__name__).upper()}     \
            \n2nd file: {(type(json_2nd).__name__).upper()}')
    elif compare_param == ('-fs' or '-sf'):
        diff = Differ(json_1st, json_2nd, print_param=True, paths=paths) 
        with open('result.json', 'w') as file: 
            file.write(json.dumps(diff.logging_analysis))
        print('\nFile saved')
    elif compare_param == '-f':
        diff = Differ(json_1st, json_2nd, print_param=False, paths=paths) 
        with open('result.json', 'w') as file: 
            file.write(json.dumps(diff.logging_analysis))
        print('File saved')
    else:
        diff = Differ(json_1st, json_2nd, print_param=True, paths=paths)
    
    return None


if __name__ == '__main__':
    try:
        path_one = sys.argv[1]
        path_two = sys.argv[2]
    except IndexError:
        print("Damn! My program require 2 paths (relative or absolute)")
        sys.exit(1)
    try:
        param = sys.argv[3] 
        compare_n_output(path_one, path_two, compare_param=param) 
    except IndexError:
        compare_n_output(path_one, path_two)