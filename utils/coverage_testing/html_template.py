__all__ = ('HTML_TOP', 'HTML_BOTTOM')

HTML_TOP = """\
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
  <head>
    <meta http-equiv="Content-type" content="text/html;charset=UTF-8" />
    <title>Code coverage report: %s</title>
    <style type="text/css" media="screen">
      ol {
        font-family:"Courier New",Courier,mono;
        padding:1em 0 1em 2.8em;
        width:90%%;
      }

      ol li {
        font-size:small;
      }
        
      ol code {
        padding:0 0 0 .2em;
        font-size:medium;
        white-space:pre;
      }
    </style>
  </head>

  <body>
"""

HTML_BOTTOM = """\
  </body>
</html>
"""