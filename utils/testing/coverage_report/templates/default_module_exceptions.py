import time

test_timestamp = time.strftime('%a %Y-%m-%d %H:%M %Z')

TOP = """\
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
  <head>
    <meta http-equiv="Content-type" content="text/html;charset=UTF-8" />
    <title>Test coverage report: %(title)s</title>
    <style type="text/css" media="screen">
      body
      {
        font-family: "Lucida Sans Unicode", "Lucida Grande", sans-serif;
        font-size: 13px;
      }
      
      #content-header
      {
        margin-left: 50px;
      }

      #content-header h1
      {
        font-size: 18px;
        margin-bottom: 0;
      }

      #content-header p
      {
        font-size: 13px;
        margin: 0;
        color: #909090;
      }
      
      #result-list
      {
        margin: 0 50px;
      }
      
      #result-list ul
      {
        padding-left: 13px;
        list-style-position: inside;
      }
   </style>
  </head>

  <body>
"""

CONTENT_HEADER = """\
<div id="content-header">
  <h1>Test Coverage Report: %(title)s</h1>"""
CONTENT_HEADER += "<p>Generated: %(test_timestamp)s</p>" %vars()
CONTENT_HEADER += "</div>"

CONTENT_BODY = """\
<div id="result-list">
  <p>%(long_desc)s</p>
  <ul>
    %(exception_list)s
  </ul>
  Back to <a href="index.html">index</a>.
</div>
"""

EXCEPTION_LINE = "<li>%(module_name)s</li>"

BOTTOM = """\
  </body>
</html>
"""