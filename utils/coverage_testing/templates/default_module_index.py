TOP = """\
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
  <head>
    <meta http-equiv="Content-type" content="text/html;charset=UTF-8" />
    <title>Code coverage report</title>
    <style type="text/css" media="screen">
      a
      {
        color: #3d707a;
      }
      
      a:hover, a:active
      {
        color: #bf7d18;
      }
    
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
      
      #result-list table
      {
        font-size: 13px;
        background: white;
        margin: 15px 50px;
        width: 600px;
        border-collapse: collapse;
        text-align: right;
      }

      #result-list thead tr.last th,
      th.lines-of-code
      {
        border-bottom: 1px solid #6d5e48;
      }
      
      th.lines-of-code
      {
        text-align: center;
      }

      #result-list th
      {
        padding: 3px 12px;
        font-size: 14px;
        font-weight: normal;
        color: #937F61;
      }

      #result-list td
      {
        border-bottom: 1px solid #e0e0e0;
        color: #606060;
        padding: 6px 12px;
      }
      
      #result-list tfoot td
      {
        color: #937F61;
        font-weight: bold;
      }

      #result-list .normal
      {
        color: #609030;
      }

      #result-list .warning
      {
        color: #d0a000;
      }

      #result-list .critical
      {
        color: red;
      }

      #result-list .module-name
      {
        text-align: left;
      }
   </style>
  </head>

  <body>
"""

CONTENT_HEADER = """\
<div id="content-header">
  <h1>Test Coverage Report</h1>
  <p>Generated: %(test_timestamp)s</p>
</div>
"""

CONTENT_BODY = """\
<div id="result-list">
  <table>
    <thead>
      <tr>
        <th>&nbsp;</th>
        <th colspan="3" class="lines-of-code">Lines of code</th>
      </tr>
      <tr class="last">
        <th class="module-name">Module</th>
        <th>total</th>
        <th>executed</th>
        <th>excluded</th>
        <th>%% covered</th>
      </tr>
    </thead>
    <tbody>
      %(module_stats)s
    </tbody>
    <tfoot>
      <tr>
        <td class="module-name">Total</td>
        <td>%(total_lines)d</td>
        <td>%(total_executed)d</td>
        <td>%(total_excluded)d</td>
        <td>%(overall_covered)0.1f%%</td>
      </tr>
    </tfoot>
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