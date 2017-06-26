from __future__ import absolute_import, unicode_literals

import logging
from cactus.site import Site
from bs4 import BeautifulSoup
import requests
from urlparse import urlparse

logger = logging.getLogger(__name__)

server = 'http://127.0.0.1:8000'


def test():
    site = Site('.')

    for page in site.pages():

        # pretty urls
        url = page.absolute_final_url.replace('.html', '/')
        full_url = server + url

        # Use title or fallback to url
        title = page.context().get('title', url)

        def check_links(u):
            return check_for_404s(u)

        check_links.description = 'Check for broken links: {}'.format(title)
        yield check_links, full_url

        def check_images(u):
            return check_for_broken_images(u)

        check_images.description = 'Check images on page: {}'.format(title)
        yield check_images, full_url


def check_for_404s(url):

    html = get_page(url)
    bs = BeautifulSoup(html)
    anchors = bs.find_all('a')
    error = False

    for anchor in anchors:
        href = anchor['href']
        logger.info('{} -> {!r}'.format(url, href))

        try:
            if is_external(href):
                logger.info('External page: {!r}'.format(href))
                get_page(href)
            else:
                logger.info('Internal link: {}'.format(href))

                # pretty urls
                if href.endswith('.html'):
                    href = href.replace('.html', '')

                full_url = server + href
                get_page(full_url)

        except requests.exceptions.InvalidURL:
            logger.error('Invalid link on page {} -> {}'.format(url, href))
            error = True
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                logger.error('Missing link on page {} -> {}'.format(url, href))
                error = True
    if error:
        raise ValueError('One or more errors on page {}'.format(url))


def check_for_broken_images(url):
    pass


def get_page(url):
    r = requests.get(url)
    r.raise_for_status()
    # TODO check headers
    return r.text


def is_external(href):
    """ Returns if a link target is relative or absolute """

    if href == '/':
        return False

    parsed = urlparse(href)
    return bool(parsed.netloc)
