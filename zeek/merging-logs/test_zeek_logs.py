"""
    Run this command before test:
        ln -s ../../data/logs logs
"""

import pytest
import os
import zeek_merger

PATH = '/logs/'

def test_logs_valid_file():
    assert os.path.isfile(PATH + "ssl.log"), 'This file is invalid'
    assert os.path.isfile(PATH + "conn.log"), 'This file is invalid'
    assert os.path.isfile(PATH + "http.log"), 'This file is invalid'
    assert os.path.isfile(PATH + "x509.log"), 'This file is invalid'

def test_dataframe_in_formatcsv():
    df = zeek_merger.format_csv(PATH + "ssl.log")
    df = zeek_merger.format_csv(PATH + "conn.log")
    df = zeek_merger.format_csv(PATH + "http.log")
    df = zeek_merger.format_csv(PATH + "x509.log")
    assert not df.empty, 'Data in ssl is empty'
    assert not df.empty, 'Data in connect is empty'
    assert not df.empty, 'Data in http is empty'
    assert not df.empty, 'Data in x509 is empty'
    print(len(df))

def test_merge_log():
    print(zeek_merger.merge_logs())
    assert zeek_merger.merge_logs(), 'Merge logs was failed'

def test_files_modified():
    assert zeek_merger.files_modified(), 'This files are not modified'

if __name__== '__main__':
    test_logs_valid_file()
    test_dataframe_in_formatcsv()
    test_merge_log()
    test_files_modified