from bs4 import BeautifulSoup as Bs

def get_html_source(tag_element):
    soup_html = Bs(tag_element.get_attribute("outerHTML"), features="lxml").prettify()
    return soup_html.removeprefix("<html>\n <body>\n").removesuffix("\n </body>\n</html>")


def print_html(tag_element, logger = None):
    for_logging = get_html_source(tag_element)
    if logger:
        logger.info(for_logging)
    else:
        print(for_logging)
