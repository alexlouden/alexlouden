import re
from cactus.template_tags import register


template = '<a href="{url}"><img src="{url}" alt="" title="{title}"></a>'


def lightbox(content):

    # Convert markdown iamge on each newline into gallery
    lines = [line for line in content.splitlines() if line]

    html = ''

    for line in lines:
        try:
            title, url = re.match('!\[(.*)\]\((.+)\)', line).groups()
            html += template.format(title=title, url=url)
        except Exception as e:
            print line, e

    return '<div class="gallery">' + html + '</div>'


def preBuild(site):
    print 'preBuild lightbox'
    register.filter('lightbox', lightbox)
