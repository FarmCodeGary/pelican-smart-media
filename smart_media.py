import logging

from bs4 import BeautifulSoup
from pelican import signals, utils


def wrap_all_embeds(generators):
    """Wrap any iframe tags in any articles or pages with Bootstrap 3's responsive embed."""
    context = generators[0].context
    for article in context['articles']:
        wrap_embed(article)
    for article in context['drafts']:
        wrap_embed(article)
    for page in context['pages']:
        wrap_embed(page)
    for page in context['hidden_pages']:
        wrap_embed(page)
    for page in context['draft_pages']:
        wrap_embed(page)

def wrap_embed(obj):
    """Wrap any iframe tags in the article or page with Bootstrap 3's responsive embed."""
    soup = BeautifulSoup(obj._content, 'html.parser')
    for iframe in soup.find_all("iframe"):
        logging.debug("Found iframe: "+iframe["src"]+" in "+obj.title)
        # iframe["class"].append("embed-responsive-item")
        div = iframe.wrap(soup.new_tag('div'))
        div["class"] = "embed-responsive embed-responsive-16by9 img-rounded"
    obj._content = soup.prettify()

def register():
    signals.all_generators_finalized.connect(wrap_all_embeds)
