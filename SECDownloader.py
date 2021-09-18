from sec_edgar_downloader import Downloader

def downloadSEC(article_type, ticker, path_to_save, amount_of_articles):
    """
    :param article_type: (Str)'10-Q' or '10-K'
    :param ticker: (Str) ticker to download
    :param path_to_save: (str) path to save the article
    :param amount_of_articles: (int) number of articles to download
    :return: HTML and Text of the 10Q or 10K documents
    """
    dl = Downloader(path_to_save)
    dl.get(article_type, ticker, amount=amount_of_articles)