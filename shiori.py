#!python3

from os import listdir
from os.path import isfile, isdir, join, splitext
import logging
import codecs
import argparse
import importlib
import sys

import ultraparse

class LibraryManager:
    def __init__(self, directory):
        self.directory = directory
        self.library = []

    def scan(self):
        self.scan_directory(self.directory)

    def scan_directory(self, directory):
        subdirs = [f for f in listdir(directory) if isdir(join(directory, f))]
        if len(subdirs) == 0:
            #No subdirectories, so this might be an ultrastar songdir
            files = [f for f in listdir(directory) if isfile(join(directory, f))]
            if self.is_songdir(files):
                txtfiles = [t for t in files if splitext(t)[1] == ".txt"]
                if (len(txtfiles) > 1):
                    logging.info("Found 2 or more text files in likely song directory " + directory)
                    map(lambda n: self.parse_songfile(join(directory, n), directory), txtfiles)
                elif (len(txtfiles) == 0):
                    logging.warning("Could not find text file in likely song directory " + directory)
                else:
                    logging.info("Found likely ultrastar file in directory " + directory)
                    self.parse_songfile(join(directory, txtfiles[0]), directory)
            else:
                logging.warning("Rejecting directory " + directory + "\nThis rejection is sometimes a false positive. I suggest running it again on this file.")
        else:
            #If there are subdirectories, search them
            for subdir in subdirs:
                self.scan_directory(join(directory, subdir))

    def is_songdir(self, filenames):
        #All valid songs should have an audio file and a text file
        extensions = list(map(lambda n: (splitext(n)[1]).upper(), filenames))
        if (not (".mp3".upper() in extensions or ".ogg".upper() in extensions or ".aac".upper() in extensions) and 
            not (".mp4".upper() in extensions or ".avi" in extensions)):
            logging.error("No sound or video file found for the following directory!")
            return False
        if (not ".txt".upper() in extensions):
            logging.error("No txt file found for the following directory!")
            return False
        return True

    def parse_songfile(self, filename, dir):
        logging.info("Now parsing file" + filename)
        try:
            #Is it UTF-8?
            f = open(filename, encoding="utf-8-sig", errors="strict")
            f.seek(0)
            song_data = ultraparse.SongFile(iter(f.readlines()), filename, dir)
            if song_data.parse():
                self.library.append(song_data)
            f.close()
        except UnicodeDecodeError:
            #Apparently not, just let python take a guess
            try:
                f = open(filename, encoding=None, errors="replace")
                song_data = ultraparse.SongFile(iter(f.readlines()), filename, dir)
                if song_data.parse():
                    self.library.append(song_data)
                f.close()
            except UnicodeDecodeError as e:
                logging.error("well balls, apparently the encoding is wonky in file " + filename + "; " + str(e))
        except Exception as e:
            logging.error("Encountered unexpected error parsing file " + filename + ":\n")
            logging.exception(e)

def run_scan():
    parser = argparse.ArgumentParser(description = "Scan directory for ultrastar songs, then export them in a given format")
    parser.add_argument('dir', metavar='dir', default="./", type=str,
                        help="the path to the directory which should be scanned")
    parser.add_argument('store', metavar='store', default="json", type=str,
                        help="the backend which should be used to export song data")
    parser.add_argument('--load-covers', action='store_true', dest='covers',
                        help="also load image files for the covers")
    parser.add_argument('--load-bg', action='store_true', dest='bgs',
                        help="also load image files for the background images")
    parser.add_argument('--include-playback-specific', action='store_true', dest='pb_specific',
                        help="include data which should only be relevant on the playback machine, such as file paths and offset timings")
    parser.add_argument('--export-opts', metavar='opts', default="", dest='opts',
                        type=str,
                        help="options to be passed to the exporter backend in the format `key1=val1,key2=val2...`")

    args = parser.parse_args()
    backend = importlib.import_module("export_formats." + args.store)
    lib = LibraryManager(args.dir)
    lib.scan()
    print ("Found " + str(len(lib.library)) + " results. Now exporting...")
    backend.export(args, parse_opts(args.opts), lib)

def parse_opts(option_string):
    entries = filter((lambda e: e != ""), option_string.split(","))
    opts_dict = {}
    for entry in entries:
        [key, value] = entry.split("=", 1)
        opts_dict[key] = value
    return opts_dict

class LessThanFilter(logging.Filter):
    def __init__(self, exclusive_maximum, name=""):
        super(LessThanFilter, self).__init__(name)
        self.max_level = exclusive_maximum

    def filter(self, record):
        #non-zero return means we log this message
        return 1 if record.levelno < self.max_level else 0

if __name__ == "__main__":
    #Check python version
    if sys.version_info < (3, 0):
        print("This script is written for python 3. Now exiting...")
        exit()
    #Get the root logger
    logger = logging.getLogger()
    #Have to set the root logger level, it defaults to logging.WARNING
    logger.setLevel(logging.NOTSET)

    logging_handler_out = logging.StreamHandler(sys.stdout)
    logging_handler_out.setLevel(logging.DEBUG)
    logging_handler_out.addFilter(LessThanFilter(logging.WARNING))
    logger.addHandler(logging_handler_out)

    # Uncomment to print it out to stderr
    # logging_handler_err = logging.StreamHandler(sys.stderr)
    logging_handler_err = logging.FileHandler('shiori_error.log', 'w', 'utf-8')
    logging_handler_err.setLevel(logging.WARNING)
    logger.addHandler(logging_handler_err)
    run_scan()
