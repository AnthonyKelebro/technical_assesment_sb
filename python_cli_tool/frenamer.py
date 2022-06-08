'''
cli-tool for renaming file with custom suffix and prefix.
'''
import os
import sys
import logging
import argparse
import tempfile
import random
from datetime import datetime, timezone

# Initialize logging and configure formater
logger = logging.getLogger('file_renamer')
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
formatter = logging.Formatter(
    fmt='%(asctime)s [%(name)s] (%(levelname)s) %(message)s',
    datefmt='[%Y-%m-%d %I:%M:%S %p]')
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


def arg_parser() -> object:
    '''
    Initialize parser for cli arguments
    :return: object
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--prefix', default='audiofile',
                        help='Prefix for renamed files (default: [audiofile])')
    parser.add_argument('-s', '--suffix', default='wav',
                        help='Suffix for finded files (default: [wav]')
    parser.add_argument('--path', default=os.getcwd(),
                        help=f'Path to directory with files (default: current directory for search:  [{os.getcwd()}/])')
    parser.add_argument('--reverse_order', action="store_true",
                        help='Rename files in reverse-alphabetical order (default: [False])')
    parser.add_argument('--debug', action="store_true",
                        help='Debug mode for testinc cli-tool (defaults: [False])')
    return parser


def debug_create_files(path_to_directory, suffix) -> None:
    '''
    Function for debug mode. Create files with suffix from arguments and files with
    wrong suffix for test mechanism.
    :return: None
    '''
    with open("/usr/share/dict/words", 'r', encoding='utf-8') as file:
        words_list = file.read().splitlines()
    # Create files with suffix from arguments
    for _ in range(20):
        file_name = f'{random.choice(words_list)}_{random.choice(words_list)}.{suffix}'
        with open(f'{path_to_directory}/{file_name}', 'w', encoding='utf-8') as file:
            pass
        logger.info('File creation for debug: File with name <%s> created', file_name)
    # Create files with wrong suffix for tests
    for _ in range(5):
        file_name = f'{random.choice(words_list)}_{random.choice(words_list)}.{suffix}rw'
        with open(f'{path_to_directory}/{file_name}', 'w', encoding='utf-8') as file:
            file.close()
        logger.info('File creation for debug: File with name <%s> created', file_name)


def get_files_from_folder(path_to_directory, suffix, reverse_order) -> list:
    '''
    Get all files from directory and return list in sorted or reverse sorted
    sequences (depends on argument).
    :return: list(str)
    '''
    list_with_file_paths = []
    for file in os.listdir(path_to_directory):
        if file.endswith(suffix):
            logger.info('Gathering data: File <%s> finded in directory', file)
            list_with_file_paths.append(file)
        else:
            logger.info('Gathering data: File <%s> not compared with current suffix - not used',
                        file)
    return sorted(list_with_file_paths,
                  reverse=True) if reverse_order else sorted(list_with_file_paths)


def file_renaming(path_to_directory, list_of_files, prefix, suffix) -> None:
    '''
    File renaming with datestamps and counters in name
    :return: None
    '''
    for count, file in enumerate(list_of_files):
        file_datestamp = datetime.fromtimestamp(
            os.stat(f'{path_to_directory}/{file}').st_ctime,
            tz=timezone.utc).strftime('%Y-%m-%d')
        new_file_name = f'{prefix}_{file_datestamp}_{count:03}.{suffix}'
        os.rename(f'{path_to_directory}/{file}', f'{path_to_directory}/{new_file_name}')
        logger.info('Renaming: File <%s> renamed to <%s>', file, new_file_name)


def main():
    '''
    Start function with initialize argument parser and main operations.
    '''
    parser = arg_parser()
    arg = parser.parse_args(sys.argv[1:])
    if arg.debug:
        with tempfile.TemporaryDirectory() as tmpdir:
            logger.info('cli-tool run in DEBUG mode.')
            debug_create_files(tmpdir, arg.suffix)
            list_files = get_files_from_folder(tmpdir, arg.suffix, arg.reverse_order)
            file_renaming(tmpdir, list_files, arg.prefix, arg.suffix)
            input(f'''
                Please check all changed files in [{tmpdir}].
                WARNING: All files and directories be removed after input.

                Waiting input from user ...
                  '''.replace('                ', ''))
    else:
        list_files = get_files_from_folder(arg.path, arg.suffix, arg.reverse_order)
        file_renaming(arg.path, list_files, arg.prefix, arg.suffix)

if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        logger.error('Script failed with next error:\n\n%s', exc)
        raise
