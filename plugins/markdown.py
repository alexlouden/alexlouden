""" Custom markdown filter, designed to be used with Prism syntax highlighting
See http://prismjs.com/

Usage:
{% filter mymarkdown %}

```python
print 'hello'!
```
{% endfilter %}

Output:
<pre><code class="language-python">
print 'hello'!
</code></pre>

"""
import sys
sys.path.insert(1, '/usr/local/lib/python2.7/site-packages')

from markdown import markdown
from markdown.extensions.fenced_code import FencedCodeExtension, FencedBlockPreprocessor

from cactus.template_tags import register


class PrismCodeExtension(FencedCodeExtension):

    def extendMarkdown(self, md, md_globals):
        """ Add FencedBlockPreprocessor to the Markdown instance. """
        md.registerExtension(self)

        md.preprocessors.add('fenced_code_block',
                             LanguageClassPreprocessor(md),
                             ">normalize_whitespace")


class LanguageClassPreprocessor(FencedBlockPreprocessor):
    """ Override to add language- to code class, to suit Prism syntax highlighting
    Example output: <code style="language-python>
    """
    LANG_TAG = ' class="language-%s"'


def mymarkdown(content):
    return markdown(
        content,
        extensions=[
            PrismCodeExtension()
        ]
    )


def preBuild(site):
    register.filter('markdown', mymarkdown)
