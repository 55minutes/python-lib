TOP = """\
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
  <head>
    <meta http-equiv="Content-type" content="text/html;charset=UTF-8" />
    <title>Code coverage report: %(title)s</title>
    <style type="text/css" media="screen">
      body {
        font-family:"Lucida Sans Unicode", "Lucida Grande", Sans-Serif;
      }
      
      .nav {
        font-size:12px;
        margin-left:2.8em;
      }

      .module_name {
        font-size:16px;
      }
    
      #content-header {
        font-size:12px;
        padding:1em 0 1em 2.8em;
      }

      #content-header h1 {
        margin:10px 0 0 0;
        color:blue;
      }
    
      #content-header p {
        margin:0;
        color:#999;
      }

      #content-header span {
        font-weight:bold;
      }
      
      #content-header span.normal {
        color:green;
      }
      #content-header span.warning {
        color:#ffcc00;
      }
      #content-header span.critical {
        color:red;
      }
      
      #source-listing {
        margin-bottom:1.5em;
      }

      #source-listing ol {
        font-family:monospace;
        padding:0 0 0 2.8em;
        width:90%%;
      }

      #source-listing ol li {
        font-size:small;
      }
        
      #source-listing ol code {
        padding:0 0 0 .2em;
        font-size:medium;
        white-space:pre;
      }
      
      #source-listing li.normal {
        color:gray;
      }
      #source-listing li.executed {
        color:#669933;
      }
      #source-listing li.missed {
        color:red;
        font-weight:bold;
      }
      #source-listing li.excluded {
        color:#6699ff;
        font-weight:lighter;
      }
   </style>
  </head>

  <body>
"""

NAV = """\
<div class="nav">
  <a href="%(prev_link)s">%(prev_label)s</a> &lt;&lt;
  <a href="%(up_link)s">%(up_label)s</a>
  &gt;&gt; <a href="%(next_link)s">%(next_label)s</a>
</div>
"""

NAV_NO_PREV = """\
<div class="nav">
  <a href="%(up_link)s">%(up_label)s</a>
  &gt;&gt; <a href="%(next_link)s">%(next_label)s</a>
</div>
"""

NAV_NO_NEXT = """\
<div class="nav">
  <a href="%(prev_link)s">%(prev_label)s</a> &lt;&lt;
  <a href="%(up_link)s">%(up_label)s</a>
</div>
"""

CONTENT_HEADER = """\
<div id="content-header">
  <h1 class="module_name">%(title)s</h1>
  <p>Source file: <span>%(source_file)s</span></p>
  <p>Stats: <span>%(total_count)d lines, %(executed_count)d executed, 
  %(excluded_count)d excluded: <span 
  class="%(severity)s">%(percent_covered)0.1f%% covered</span></span></p> 
  <p>Generated: <span>%(test_timestamp)s</span></p>
</div>
"""

CONTENT_BODY = """\
<div id="source-listing">
  <ol>
    %(source_lines)s
  </ol>
</div>
"""

SOURCE_LINE = '<li class="%(line_status)s"><code>%(source_line)s</code></li>'

BOTTOM = """\
  </body>
</html>
"""