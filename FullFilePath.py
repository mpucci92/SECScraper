import glob as glob

def createFullPath(tickers):
    """
    :param tickers: List that contains financial tickers
    :return: file path to where 10Q and 10K files are located
    """

    full_file_path = []

    for ticker in tickers:
        path = fr"C:\Users\mp094\Desktop\SEC_Financial_documents\sec-edgar-filings\{ticker}"

        for file in glob.glob(path, recursive=True):
            for path1 in glob.glob(file + '\*'):
                for path2 in glob.glob(path1 + '\*'):
                    for path3 in glob.glob(path2 + '\*.txt'):
                        full_file_path.append(path3)

    return full_file_path


def createFullPathSolo(ticker):
    """
    :param ticker: Individual ticker
    :return: file path to where 10Q and 10K files are located
    """

    full_file_path = []

    path = fr"C:\Users\mp094\Desktop\SEC_Financial_documents\sec-edgar-filings\{ticker}"

    for file in glob.glob(path, recursive=True):
        for path1 in glob.glob(file + '\*'):
            for path2 in glob.glob(path1 + '\*'):
                for path3 in glob.glob(path2 + '\*.txt'):
                    full_file_path.append(path3)

    return full_file_path