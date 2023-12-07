import newspaper as news
import nltk
import regex as re
nltk.download('punkt')

def rawtext_from_url(url):
    article = news.Article(url)
    article.download()
    article.parse()

    return article.text


