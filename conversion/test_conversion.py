from os.path import exists, basename, dirname, abspath
from shutil import rmtree, copytree, copy
from argparse import ArgumentParser
from multiprocessing import Pool
from subprocess import Popen
from filecmp import cmp
from re import findall
from glob import glob
from os import mkdir


def get_testing_program_path():
    parser = ArgumentParser()
    parser.add_argument("conversion_program_path", type=str)
    args = parser.parse_args()
    return args.conversion_program_path


def prepare_environment(program_path):
    if exists("runtime"):
        rmtree("runtime", ignore_errors=True)
    mkdir("runtime")

    copytree("./tests", "./runtime/tests")

    for path in glob("./runtime/tests/**/input.txt"):
        copy(program_path, dirname(path))


def run_test(args):
    def get_executor(exe_name):
        extension = exe_name.split(".")[-1]
        if extension == "py":
            return "python"
        elif extension == "jar":
            return "java"
        else:
            return None

    exe_path, dir_path = args
    dir_path = dirname(dir_path)
    with open(f"{dir_path}/input.txt") as inp, open(f"{dir_path}/output.txt", "w") as outp:
        dir_path = abspath(dir_path)
        Popen(list(filter(lambda value: value is not None, [get_executor(basename(exe_path)),
                                                            f"{dir_path}/{exe_path}", "input.txt", "output.txt"])),
              stdin=inp,
              stdout=outp,
              cwd=dir_path).wait()


def run_tests(exe_path):
    args = [(exe_path, input_dir) for input_dir in glob("./runtime/tests/**/input.txt")]
    Pool(len(args)).map(run_test, args)


def print_result(test_name, conversion_result, graphiz_result):
    print(f"{test_name}:")
    print(f"  * Conversion: {'OK' if conversion_result else 'Failed'}")
    print(f"  * Graphiz: {'OK' if graphiz_result else 'Failed'}")
    print()


def check_results():
    for path in glob("./runtime/tests/**/output.txt"):
        path = dirname(path)
        with open(f"{path}/expected_output.txt") as expected_outp, open(f"{path}/output.txt") as outp:
            result = [int(num) for num in findall(r"\d+", " ".join(outp.read().splitlines()))]
            expected_result = [int(num) for num in findall(r"\d+", " ".join(expected_outp.read().splitlines()))]
            dots = [basename(path) for path in glob(f"{path}/*.dot")]

            conversion_result = result == expected_result
            graphiz_result = (len(dots) == 2) and cmp(f'{path}/{dots[0]}', f'{path}/{dots[1]}')
            print_result(basename(path), conversion_result, graphiz_result)


def main():
    program_path = get_testing_program_path()

    prepare_environment(program_path)
    run_tests(basename(program_path))
    check_results()


if __name__ == "__main__":
    main()
