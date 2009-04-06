TOP = """\
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
  <head>
    <meta http-equiv="Content-type" content="text/html;charset=UTF-8" />
    <title>Code coverage report</title>
    <style type="text/css" media="screen">
      body {
        font-family: "Lucida Sans Unicode", "Lucida Grande", Sans-Serif;
      }
      
      #content-header {
        margin-left:45px;
      }
      #content-header h1 {
        font-size:18px;
        margin-bottom:0;
      }
      #content-header p {
        font-size:14px;
        margin:0;
        color:#999;
      }
      
      #result-list table {
        font-size: 13px;
        background: #fff;
        margin: 15px 45px;
        width: 600px;
        border-collapse: collapse;
        text-align: right;
      }
      #result-list thead {
        border-bottom: 2px solid #6678b1;
      }
      #result-list th {
        font-size: 14px;
        font-weight: normal;
        color: #039;
        padding: 0 12px;
      }
      #result-list td {
        border-bottom: 1px solid #ccc;
        color: #669;
        padding: 6px 12px;
      }

      #result-list .normal {
        color:green;
      }
      #result-list .warning {
        color:yellow;
      }
      #result-list .critical {
        color:red;
      }
      #result-list .module-name {
        text-align:left;
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
      <tr style="text-align:center;">
        <th> </th>
        <th colspan="3" style="border-bottom:2px solid #6678b1;">Lines of code</th>
      </tr>
      <tr>
        <th class="module-name">Module</th>
        <th>total</th>
        <th>executed</th>
        <th>excluded</th>
        <th>%% covered</th>
      </tr>
    </thead>
    <tfoot>
      <tr>
        <td class="module-name">Total</td>
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
<tr>
  <td class="module-name"><a href="%(module_link)s">%(module_name)s</a></td>
  <td>%(total_count)d</td>
  <td>%(executed_count)d</td>
  <td>%(excluded_count)d</td>
  <td class="%(severity)s">%(percent_covered)0.1f%%</td>
</tr>
"""

BOTTOM = """\
  </body>
</html>
"""