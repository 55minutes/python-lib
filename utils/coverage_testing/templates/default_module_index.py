TOP = """\
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
  <head>
    <meta http-equiv="Content-type" content="text/html;charset=UTF-8" />
    <title>Code coverage report</title>
    <style type="text/css" media="screen">
      #content-header h1 {
        font-family:sans-serif;
        margin-bottom:0;
      }
      
      #content-header p {
        margin:0;
        color:#999;
      }
      
      #result-list tr.normal {
        color:green;
      }
      #result-list tr.warning {
        color:yellow;
      }
      #result-list tr.critical {
        color:red;
      }
   </style>
  </head>

  <body>
"""

CONTENT_HEADER = """\
<div id="content-header">
  <h1>Coverage Report</h1>
  <p>Generated: <span>%(test_timestamp)s</span></p>
</div>
"""

CONTENT_BODY = """\
<div id="result-list">
  <table>
    <thead>
      <tr>
        <th> </th>
        <th colspan="3">Lines of code</th>
      </tr>
      <tr>
        <th>Module</th>
        <th>total</th>
        <th>executed</th>
        <th>excluded</th>
        <th>%% covered</th>
      </tr>
    </thead>
    <tfoot>
      <tr>
        <td>Total</td>
        <td>%(total_lines)d</td>
        <td>%(total_executed)d</td>
        <td>%(total_excluded)d</td>
        <td>%(overall_covered)0.1f%%</td>
      </tr>
    </tfoot>
    <tbody>
      %(module_stats)s
    </tbody>
  </table>
</div>
"""

MODULE_STAT = """\
<tr class="%(severity)s">
  <td class="module-name"><a href="%(module_link)s">%(module_name)s</a></td>
  <td>%(total_count)d</td>
  <td>%(executed_count)d</td>
  <td>%(excluded_count)d</td>
  <td>%(percent_covered)0.1f%%</td>
</tr>
"""

BOTTOM = """\
  </body>
</html>
"""