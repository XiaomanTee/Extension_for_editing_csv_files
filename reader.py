import os
import sys
import csv
import json
import pickle

class File:
    def __init__(self, src, dst, changes):
        self.src = src
        self.dst = dst
        self.changes = changes

    def read_file(self):
        pass

    def write_file(self, data):
        pass

    def make_changes(self):
        data = self.read_file()

        for change in self.changes:
            X, Y, value = map(str.strip, change.split(",", 2))
            X = int(X)
            Y = int(Y)
            data[Y][X] = value

        self.write_file(data)
        self.display_data(data)

    def display_data(self, data):
        for data in data:
            print(",".join(data))

class CSVFile(File):
    def read_file(self):
        try:
            with open(self.src, newline = "") as f:
                reader = csv.reader(f)
                data = list(reader)
                return data 
        except FileNotFoundError:
            print(f"Error: File {self.src} not found")
            directory = os.path.abspath(self.src)
            directory_name = os.path.dirname(directory)
            print("Exist files: ")

            for files in os.listdir(directory_name):
                print(files, end = " ")
            
            sys.exit(1)

    def write_file(self, data):
        with open(self.dst, 'w', newline = "") as f:
            writer = csv.writer(f)
            writer.writerows(data)

class JSONFile(File):
    def read_file(self):
        try:
            with open(self.src, 'r') as f:
                return json.load(f)
        except:
            print(f"Error: File {self.src} not found")
            directory = os.path.abspath(self.src)
            directory_name = os.path.dirname(directory)
            print("Exist files: ")

            for files in os.listdir(directory_name):
                print(files, end = " ")

            sys.exit(1)

    def write_file(self, data):
        with open(self.dst, 'w') as f:
            json.dump(data, f)

class PickleFile(File):
    def read_file(self):
        try:
            with open(self.src, 'rb') as f:
                return pickle.load(f)
        except:
            print(f"Error: File {self.src} not found")
            directory = os.path.abspath(self.src)
            directory_name = os.path.dirname(directory)
            print("Exist files: ")

            for files in os.listdir(directory_name):
                print(files, end = " ")

            sys.exit(1)

    def write_file(self, data):
        with open(self.dst, 'wb') as f:
            pickle.dump(data, f)

def check_source(src, dst, changes):
    src_file = os.path.splitext(src)[-1].lower()

    if src_file == ".csv":
        return CSVFile(src, dst, changes)
    elif src_file == ".json":
        return JSONFile(src, dst, changes)
    elif src_file == ".pickle":
        return PickleFile(src, dst, changes)
    else:
        print("Error: Source file path format not support")
        sys.exit(1)

def check_dst(dst):
    dst_file = os.path.splitext(dst)[-1].lower()

    if dst_file == ".csv" or dst_file == ".json" or dst_file == ".pickle":
        return dst
    else:
        print("Error: Destination file path format not support")
        sys.exit(1)

def main():
    if len(sys.argv) < 4:
        print("The script should be run as: reader.py <src> <dst> <change1> <chnage2> ... ")
        sys.exit(1)

    src = sys.argv[1]
    dst = sys.argv[2]
    changes = sys.argv[3:]

    check_dst(dst)

    modifier = check_source(src, dst, changes)
    modifier.make_changes()

if __name__ == "__main__":
    main()
