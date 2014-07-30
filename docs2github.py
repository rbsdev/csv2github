#!/usr/bin/env python3
import sys
import parse_csv_docs
import csv, codecs

if __name__ == "__main__":
	parse_csv_docs.extract_issues(sys.argv[1])