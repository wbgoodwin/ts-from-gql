import argparse

def fail_ts_generation(failure_message):
    print("TS generation unsuccessful:")
    print("     " + failure_message)
    exit(1)

def write_to_file():
    print()

def read_file():
    print()

def generate_ts():
    print("hello")

def verify_input_file():
    print("gql or graphql (or json?)")

def parse_cli_args():
    parser = argparse.ArgumentParser()
    
    parser.add_argument("-o", "--OutputFile", help = "The generated ts output file")
    parser.add_argument("-i", "--InputFile", help = "The input gql schema file")
    
    args = parser.parse_args()
    if not args.OutputFile or not args.InputFile:
        fail_ts_generation("Input and output file args required")

    return args


if __name__ == "__main__":
    parse_cli_args()
    verify_input_file()
    generate_ts()