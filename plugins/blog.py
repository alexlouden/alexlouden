import datetime
import logging

import sys
sys.path.insert(1, '/usr/local/lib/python2.7/site-packages')

from markdown import markdown
from markdown.extensions.fenced_code import FencedCodeExtension

from django.template import Context
from django.template.loader import get_template
from django.template.loader_tags import BlockNode, ExtendsNode

from cactus.template_tags import register


Global = {"config": {}, "posts": [], "projects": []}

Global["config"]["path"] = "posts"
Global["config"]["date_format"] = "%d-%m-%Y"
Global["config"]["post_body_block"] = "body"

by_date = lambda x: x.get("date")


def mymarkdown(content):
    return markdown(
        content,
        extensions=[
            FencedCodeExtension()
        ]
    )


def preBuild(site):

    register.filter('mymarkdown', mymarkdown)

    global Global

    for page in site.pages():

        # Skip non-html pages
        if not page.path.endswith('.html'):
            continue

        if page.path.startswith('posts/'):
            article_type = 'posts'

        elif page.path.startswith('projects/'):
            article_type = 'projects'

        else:
            continue

        context = parse_page(page)
        Global[article_type].append(context)

    # Sort the posts by date and add the next and previous page indexes
    Global["posts"] = sorted(Global["posts"], key=by_date, reverse=True)
    Global["projects"] = sorted(Global["projects"], key=by_date, reverse=True)

    indexes = xrange(0, len(Global["posts"]))

    for i in indexes:
        if i + 1 in indexes:
            Global["posts"][i]['prevPost'] = Global["posts"][i + 1]
        if i - 1 in indexes:
            Global["posts"][i]['nextPost'] = Global["posts"][i - 1]


def parse_page(page):

    context = page.context()
    context_post = {"path": page.path}

    # Check if we have the required keys
    for field in ["title", "date"]:

        if not field in context:
            logging.warning("Page %s is missing field: %s" % (page.path, field))
        else:
            if field == "date":
                # Parse date from string to datetime
                context_post[field] = parse_date(context[field], page.path)
            else:
                context_post[field] = context[field]

    # Temp post context
    temp_post_context = Context(context)
    temp_post_context.update(context_post)

    # Add the post contents
    context_post["body"] = _get_node(
        get_template(page.path),
        context=temp_post_context,
        name=Global["config"]["post_body_block"]
    )

    return context_post


def preBuildPage(site, page, context, data):

    context['posts'] = Global["posts"]
    context['projects'] = Global["projects"]

    for post in Global["posts"]:
        if post["path"] == page.path:
            context.update(post)

    for post in Global["projects"]:
        if post["path"] == page.path:
            context.update(post)

    return context, data


# Utilities for the functions above

def parse_date(date_string, path):
    # Convert a string to a date object
    try:
        return datetime.datetime.strptime(date_string, Global["config"]["date_format"])
    except Exception as e:
        msg = "Date format not correct for page {}, should be {}\n{}".format(path, Global["config"]["date_format"], e)
        logging.warning(msg)


def _get_node(template, context=Context(), name='subject'):
    # Get the contents of a block in a specific template
    for node in template:
        if isinstance(node, BlockNode) and node.name == name:
            return node.render(context)
        elif isinstance(node, ExtendsNode):
            return _get_node(node.nodelist, context, name)
    raise Exception("Node '%s' could not be found in template." % name)
