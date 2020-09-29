import sys
import os
import shutil


def exit_cli(print_func, message):
    print_func("%s" % message)
    sys.exit(0)


def display_file(file_name):
    """
    Open given file with default user program.
    """
    if sys.platform.startswith("linux"):
        os.system("xdg-open %s" % file_name)

    elif sys.platform.startswith("darwin"):
        os.system("open %s" % file_name)


def remove_dir(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print("Failed to delete %s. Reason: %s" % (file_path, e))
            exit_cli(print, "")
