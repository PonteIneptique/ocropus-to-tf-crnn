""" This CLI is kept as a single file. While it reduces it readability for development,
it enhances it capacity to be used by not requiring to keep that in your own folder.

"""
from argparse import ArgumentParser
import os.path
import sys
import os
import glob

#################################################################################
#
#  CONSTANTS
#
#################################################################################

# Not used at the moment.
CONFIG_DEFAULT = {  # From https://raw.githubusercontent.com/solivr/tf-crnn/master/config_template.json
  "training_params": {
    "learning_rate": 1e-3,
    "learning_decay_rate": 0.95,
    "learning_decay_steps": 5000,
    "save_interval": 1e3,
    "n_epochs": 50,
    "train_batch_size": 128,
    "eval_batch_size": 128
  },
  "input_shape": [32, 304],
  "string_split_delimiter": "|",
  "csv_delimiter": ";",
  "lookup_alphabet_file": "./tf_crnn/data/lookup_letters_digits_symbols.json",
  "csv_files_train": ["./my_train_data.csv"],
  "csv_files_eval": ["./my_eval_data.csv"],
  "output_model_dir": "/.output/"
}
SUB_COMMAND = "\t"
DEBUG = False
CHARACTERS = set()
SEPARATOR_COLUMN = ";"  # Character for the columns in CSV
SEPARATOR_CHARACTERS = "|"  # Character for separating input characters in ground truth

#################################################################################
#
#  Function
#
#################################################################################


def print_detail(data):
    """ This function print a secondary information

    :param data: String to be printed
    """
    print(SUB_COMMAND+data)


def print_sep():
    """ Prints a separator
    """
    print("==============================")


def try_catch(callable, *args, **kwargs):
    """ This function calls a callable but wraps it with a try-catch
    Errors are raise if DEBUG is True

    :param callable: Function to call
    :param args: Arguments
    :param kwargs: Keyword Arguments
    :return: Output of the function
    """
    try:
        callable(*args, **kwargs)
    except Exception as E:
        if DEBUG:
            raise E
        print_sep()
        print("An error has occured :")
        print_detail(E.args[0])
        sys.exit(1)


def check_arguments(args):
    """ This function check the argument and their

    :param args: Check that input arguments are correct
    :return: Develop arguments
    """
    print_sep()
    print("Checking input arguments:")
    os.makedirs(args.output, exist_ok=True)
    for directory in args.directories:
        if not os.path.isdir(directory):
            raise ValueError("Directory {} does not exist".format(directory))
    print_detail("Arguments are valid.")


def ground_truth_name(filename):
    """ Compute the groundtruth filename from ocropus training file

    :param filename: Name of the image file to find ground truth for
    :return: Name of the ground truth file
    """
    return ".".join(filename.replace(".bin", "").split(".")[:-1]+["gt", "txt"])


def create_file(directory):
    fname = os.path.join(directory, "groundtruth.csv")
    with open(fname, 'w') as f:
        f.write("")
    return fname


def write_line(
        input_image, input_groundtruth,
        output_groundtruth
):
    """ Write the TF-CRNN groundtruth line for given image file and ground truth

    :param input_image: Name of the input image
    :param input_groundtruth: Name of the ground truth text file that needs to be read
    :param output_groundtruth: Name of the ground truth text file that needs to be written to
    """
    with open(input_groundtruth) as f:
        content = f.read().strip()

    # CHARACTERS.update(set(content))

    with open(output_groundtruth, "a") as f:
        f.write(
            input_image + SEPARATOR_COLUMN +  # Input path is the first column
            SEPARATOR_CHARACTERS +  # Ground truth is enclosed in `|`
            SEPARATOR_CHARACTERS.join([  # Each character in separated by a |
                char
                for char in content
            ]) +
            "\n"  # Preparing for next line
        )


def run(source=(), target="output"):
    print_sep()
    print("Transforming data")
    for source_directory in source:
        # If we have more than one input directory
        if len(source) > 1:
            target_directory = os.path.join(target, os.path.basename(source_directory))

            # We compute absolute path for easier replacement later
            abs_source_directory = os.path.abspath(source_directory)

            # We create the directory that will be necessary
            if not os.path.isdir(target_directory):
                os.makedirs(target_directory, exist_ok=True)
        else:
            target_directory = target
            abs_source_directory = os.path.abspath(target_directory)

        print_detail("Transforming {}'s data into {}'s data".format(
            source_directory, target_directory
        ))

        # Create the target file
        target_crnn_truthfile = create_file(target_directory)
        transformed = 0

        # Process each known line
        for image_file in glob.glob(os.path.join(abs_source_directory, "**/*.png"), recursive=True):
            ground_truth_file = ground_truth_name(image_file)
            write_line(
                image_file, ground_truth_file,
                target_crnn_truthfile
            )
            transformed += 1
        print_detail("{:,} lines referenced in {}".format(transformed, target_crnn_truthfile))
    print_sep()
    print_detail("Saving the character found")

#################################################################################
#
#  CLI
#
#################################################################################

cli = ArgumentParser(
    "Convert Ocropus training data into a"
    "tf-crnn format ( https://github.com/solivr/tf-crnn )"
)
cli.add_argument("directories", nargs="+",
                 help="Directory in which data are that needs to be converted are")
cli.add_argument("--output", help="Target directory in which to save the new data",
                 default=os.path.join(".", "output"))

if __name__ == "__main__":
    # Retrieve the input
    input_arguments = cli.parse_args()
    # Check their value
    try_catch(check_arguments, input_arguments)

    try_catch(run, source=input_arguments.directories, target=input_arguments.output)
