import argparse
from pathlib import Path

class CliArguments:
    def __init__(self, input_file_path, output_file_path):
        self.input_file_path = input_file_path
        self.output_file_path = output_file_path

def fail_ts_generation(failure_message):
    print("TS generation unsuccessful:")
    print("     " + failure_message)
    exit(1)

def write_to_file(output_file_path, lines_to_write):
    with open("output_file_path", "w") as file:
        file.writelines(lines_to_write)


def read_file(input_file_path):
    file_lines: list[str]
    with open(input_file_path) as file:
        file_lines = file.readlines()
    return file_lines

def line_indicates_query_or_mutation(split_line: list[str]):
    return len(split_line) == 3 and (split_line[1] == "Query" or split_line[1] == "Mutation") and "{" in split_line[2]


def remove_queries_and_mutations(lines: list[str]):
    updated_lines: list[str] = list()
    in_query_or_mutation = False
    for line in lines:
        if in_query_or_mutation and "}" in line:
            in_query_or_mutation = False
        elif not in_query_or_mutation:
            whitespace_split_str = line.split()
            if line_indicates_query_or_mutation(whitespace_split_str):
                in_query_or_mutation = True
            else:
                updated_lines.append(line)
    return updated_lines



def convert_type(input_type: str):
    # would prefer to use match-case, but that is new and want this to be
    # compatible with older versions of python.
    parsed_type = input_type.strip().split(" ")[0].replace("!", "")
    if "String" in parsed_type:
        return "string"
    elif "Int" in parsed_type:
        return "number"
    elif "UUID" in parsed_type:
        return "Uuid"
    else:
        return parsed_type


def convert_line(line: str):
    if line.lstrip().startswith("#"):
        return

    whitespace_split_str = line.split()
    if len(whitespace_split_str) == 3 and whitespace_split_str[0] == "type" and "{" in whitespace_split_str[2]:
        return line.replace("type", "interface")

    colon_split_str = line.split(":")
    if len(colon_split_str) == 2:
        return line.replace(
                colon_split_str[1],
                " " + convert_type(colon_split_str[1]) + "\n"
            )

    return line
    

def generate_ts(args: CliArguments):
    input_file_lines = read_file(args.input_file_path)
    output_file_lines: list[str] = list()
    for line in input_file_lines:
        converted_line = convert_line(line)
        if converted_line:
            output_file_lines.append(converted_line)
    output_file_lines = remove_queries_and_mutations(output_file_lines)
    write_to_file(args.output_file_path, output_file_lines)

def verify_input_file(input_file_path: str):
    if not input_file_path.endswith(".gql") and not input_file_path.endswith(".graphql"):
        fail_ts_generation("Invalid input file type. A gql file is required.")
    if not Path(input_file_path).is_file():
        fail_ts_generation("The input file '{}' does not exist".format(input_file_path))

def parse_cli_args():
    parser = argparse.ArgumentParser()
    
    parser.add_argument("-o", "--OutputFile", help = "The generated ts output file")
    parser.add_argument("-i", "--InputFile", help = "The input gql schema file")
    
    args = parser.parse_args()
    if not args.OutputFile or not args.InputFile:
        fail_ts_generation("Input and output file args required")

    return CliArguments(args.InputFile, args.OutputFile)


if __name__ == "__main__":
    args = parse_cli_args()
    verify_input_file(args.input_file_path)
    generate_ts(args)
    print("TS file generation complete.")


# Want to remove comment lines
# Remove !
# remove @deprecated?
# only convert type -> interface if it is referencing an actual gql type, not just the word happens to be there.
# String -> string