"""Deploy lectures.

Usage:
  deploy.py <input_dir> <output_dir>
  deploy.py -c <input_dir> <output_dir>

Options:
  -h --help         Show this screen.
  -c --copy-only    No compilation

"""
import os
import shutil
import logging
from pathlib import Path
from docopt import docopt
import subprocess


MAIN_DOCUMENT_NAME = "lecture_messtechnik_2.tex"
DEPLOY_PATTERNS = [
    "environment.yml",
    "content/**/*.ipynb",
    "content/**/*.py",
    "content/**/*.wav",
	"content/**/*.grc"]

IGNORE_PATTERNS = [
    ".ipynb_checkpoints"
]

def check_input_dir(input_dir):
    input_dir = Path(input_dir)
    logging.debug(f"Checking input directory {input_dir} for file {MAIN_DOCUMENT_NAME}")
    if MAIN_DOCUMENT_NAME in [os.path.basename(curfile) for curfile in input_dir.glob("*.tex")]:
        print(f'Main document file {MAIN_DOCUMENT_NAME} detected in input dir {str(input_dir)}')
    else:
        raise FileNotFoundError


def full_latex_compile(tex_file):
    # ensure working with Path objects
    tex_file = Path(tex_file)
    filename_deploy = f"{tex_file.stem}_deploy"
    working_dir = tex_file.parent
    logging.debug(f"Processing file {tex_file.with_suffix('.tex').name}")
    logging.debug(f"Using working directory {working_dir}")
    # re-compile format to get current date
    subprocess.run(["pdftex", "-ini", '-jobname="mybeamer"', "&pdflatex", 'mylatexformat.ltx', 'mybeamer.tex'], cwd=working_dir)
    # compile document
    subprocess.run(["pdflatex", "-shell-escape", f"--jobname={filename_deploy}", tex_file.with_suffix('.tex').name], cwd=working_dir)
    subprocess.run(["makeglossaries", filename_deploy], cwd=working_dir)
    subprocess.run(["biber", filename_deploy], cwd=working_dir)
    subprocess.run(["pdflatex", "-shell-escape",  f"--jobname={filename_deploy}", tex_file.with_suffix('.tex').name], cwd=working_dir)

def check_output_dir(output_dir):
    output_dir = Path(output_dir)
    if output_dir.exists():
        def ask_for_delete():
            input_str =  input(f"Delete contents of directory {output_dir} [y]/n?")
            print(f"received {input_str.lower()}")
            if (input_str.lower() == "y") or (input_str.lower() == ""):
                print("Deleting contents of directory")
                delete_all_files_in_folder(output_dir)
            elif input_str.lower() == "n":
                print("Keeping directory")
                raise FileExistsError
        ask_for_delete()
    else:
        print(f"Creating output directory: {str(output_dir)}")
        os.mkdir(output_dir)

def delete_all_files_in_folder(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

def copy_to_output_dir(input_dir, output_dir, deploy_patterns):    
    # ensure working with Path objects
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    logging.debug(f"Copying from {input_dir} to {output_dir}")
    logging.debug(f"Input dir has the parts {input_dir.parts}, number of parts is {len(input_dir.parts)}")
    # copy PDF file
    pdf_file_src =  Path(os.path.splitext(MAIN_DOCUMENT_NAME)[0] + '_deploy').with_suffix('.pdf')
    pdf_file_dst =  Path(MAIN_DOCUMENT_NAME).with_suffix('.pdf')
    print(f"Copying PDF file: {pdf_file_src} to {pdf_file_dst}")
    shutil.copy2(input_dir / pdf_file_src, output_dir / pdf_file_dst)
    for current_deploy_pattern in deploy_patterns:
        logging.debug(f"Processing deploy pattern {current_deploy_pattern}")
        # copy all files matching current deploy pattern
        for curfile in input_dir.glob(current_deploy_pattern):
            if "/." in str(curfile.relative_to(input_dir)):
                logging.debug(f"Ignoring hidden file {curfile.relative_to(input_dir)}")
                continue
            if any(current_pattern in str(curfile.relative_to(input_dir)) for current_pattern in IGNORE_PATTERNS):
                logging.debug(f"Ignoring file {curfile.relative_to(input_dir)}")
                continue
            print(f"Copying file: {curfile.relative_to(input_dir)}")
            dst = output_dir / curfile.relative_to(input_dir)
            if not dst.parent.exists():
                os.makedirs(dst.parent)
            shutil.copy2(curfile, dst)


def deploy_from_to(input_dir, output_dir, copy_only=False, deploy_patterns = [""]):
    print("Called deploy function")
    # ensure working with Path objects
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    # check that we are in the right dir
    check_input_dir(input_dir)
    # check output dir
    check_output_dir(output_dir)
    # perform full latex compule
    if not copy_only:
        full_latex_compile(input_dir / MAIN_DOCUMENT_NAME)    
    # copy to output dir
    copy_to_output_dir(input_dir, output_dir, deploy_patterns)
    pass

if __name__ == "__main__":
    arguments = docopt(__doc__)
    print(arguments)
    logging.basicConfig(level=logging.DEBUG)
    deploy_from_to(arguments["<input_dir>"], arguments["<output_dir>"], copy_only = arguments["--copy-only"], deploy_patterns=DEPLOY_PATTERNS)
