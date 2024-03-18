# HTML stuff for errors / successful export

done='''
<!DOCTYPE html>
<html>
    <head>
        <title>Successfull Export</title>
    </head>
    <body>
            <br><br><br><br><br><br><br><br><br><br><br>
        <div align='center'>
           <p>
              <span style="font-family:'Arial';color:DarkSlateBlue;font-size:100px;"><b>Ma</b></span>
              <span style="font-family:'Arial';color:white;background-color:DarkSlateBlue;font-size:100px;"><b>RDMO</b></p></span>
           </p>
           <br><br><br>
           {}
        </div>
    </body>
</html>'''

search_done="""
<!DOCTYPE html>
<html>
    <head>
        <title>Workflows Found!</title>
    </head>
    <body>
        <br><br><br>
        <div align='center'>
           <p>
              <span style="font-family:'Arial';color:DarkSlateBlue;font-size:100px;"><b>Ma</b></span>
              <span style="font-family:'Arial';color:white;background-color:DarkSlateBlue;font-size:100px;"><b>RDMO</b></p></span>
           </p>
           <br><br><br>
           <p style="color:DarkSlateBlue;font-size:30px;">We found {0} Workflow(s) on the MaRDI Portal!</p>
           <p style="color:DarkSlateBlue;font-size:30px;">Here are the Links to the Documentations:</p>
           {1}
        </div>
    </body>
</html>"""

export='''<p style="color:DarkSlateBlue;font-size:30px;">You're Workflow has been added to the MaRDI Portal.</p>
<p style="color:DarkSlateBlue;font-size:30px;"><a href="{0}" style="color:orange;">Wiki Page</a>\t-\t<a href="{1}" style="color:orange;">Knowledge Graph Entry</a></p>'''

link='<p style="color:DarkSlateBlue;font-size:20px;">{0}  ( <a href="{1}" style="color:orange;">Wiki Page</a>\t-\t<a href="{2}" style="color:orange;">Knowledge Graph Entry</a> )</p><br>'

html="""
<head>
  <script type="text/javascript" id="MathJax-script" async
    src="https://cdn.jsdelivr.net/npm/mathjax@3.0.0/es5/tex-mml-chtml.js">
  </script>
  <style>
    table {{
      margin-left: 0;
      margin-right: auto;
      margin-bottom: 24px;
      border-spacing: 0;
      border-bottom: 2px solid black;
      border-top: 2px solid black;
    }}
    table th {{
      padding: 3px 10px;
      background-color: white;
      border-top: none;
      border-left: 1px solid black;
      border-right: 1px solid black;
      border-bottom: 1px solid black;
      text-align: center;
    }}
    table td {{
      padding: 3px 10px;
      border-top: 1px solid black;
      border-left: 1px solid black;
      border-bottom: 1px solid black;
      border-right: 1px solid black;
      text-align: center;
    }}
  </style>
</head>
<body>
{}
</body>
</html>
"""

