import re


class PrePro:
    def __init__(self):
        pass

    @staticmethod
    def read_file_line_by_line(source):
        with open(source, 'r') as f:
            lines = f.readlines()
            lines = [line for line in lines if line.strip() != '']
        return lines

    @staticmethod
    def filter(source):
        lines = PrePro.read_file_line_by_line(source)
        # Remove comments in Lua file (-- This is a comment in Lua)
        for i, line in enumerate(lines):
            lines[i] = re.sub(r"--.*", "", line)
        # Filter out empty strings
        return [line for line in lines if line.strip() != '']

