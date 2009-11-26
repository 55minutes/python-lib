import html5lib
from html5lib import sanitizer, treebuilders, treewalkers, serializer

def sanitizer_factory(*args, **kwargs):
    san = sanitizer.HTMLSanitizer(*args, **kwargs)
    # This isn't available yet
    # san.strip_tokens = True
    return san

def clean_html(buf):
    """Cleans HTML of dangerous tags and content."""
    buf = buf.strip()
    if not buf:
        return buf

    p = html5lib.HTMLParser(tree=treebuilders.getTreeBuilder("dom"),
            tokenizer=sanitizer_factory)
    dom_tree = p.parseFragment(buf)

    walker = treewalkers.getTreeWalker("dom")
    stream = walker(dom_tree)

    s = serializer.htmlserializer.HTMLSerializer(
            omit_optional_tags=False,
            quote_attr_values=True)
    return s.render(stream)

