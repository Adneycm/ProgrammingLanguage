from parser_dealer import Parser
from pre_processing import PrePro
from symbol_table import SymbolTable
import sys


if __name__ == "__main__":
    # source = sys.argv[1]
    source = "test_file.rtn"

    source_lines = PrePro.filter(source)
    source_lines = ' '.join(source_lines)

    parser = Parser()
    symbol_table = SymbolTable()

    parser.run(source=source_lines)

    if parser.tokenizer.position < len(parser.tokenizer.source):
        raise ValueError("Invalid input")

