# HTML stuff for errors / successful export

response_temp='''
<!DOCTYPE html>
<html>
    <head>
        <title>Error</title>
    </head>
    <body>
            <br><br><br><br><br><br><br><br><br><br><br>
        <div align='center'>
           <p>
              <span style="font-family:'Arial';color:DarkSlateBlue;font-size:200px;"><b>Ma</b></span>
              <span style="font-family:'Arial';color:white;background-color:DarkSlateBlue;font-size:200px;"><b>RDMO</b></p></span>
           </p>
           <br><br><br>
           {}
        </div>
    </body>
</html>'''

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
              <span style="font-family:'Arial';color:DarkSlateBlue;font-size:200px;"><b>Ma</b></span>
              <span style="font-family:'Arial';color:white;background-color:DarkSlateBlue;font-size:200px;"><b>RDMO</b></p></span>
           </p>
           <br><br><br>
           {}
        </div>
    </body>
</html>'''

export='''<p style="color:blue;font-size:30px;">You're Workflow has been added to the MaRDI Portal.</p>
<p style="color:blue;font-size:30px;"><a href="{0}" style="color:orange;">Wiki Page</a>\t<a href="{1}" style="color:orange;">Knowledge Graph Entry</a></p>'''

err='''<p style="color:red;font-size:50px;">Ooops...</p>
<p style="color:red;font-size:50px;">{}</p>'''

err1  = err.format('The Questionnaire \'{}\' is not suitable for the MaRDI Export!')
err2  = err.format('You haven\'t chosen an export type!')
err3  = err.format('You haven\'t chosen an entity to search for!')
err4  = err.format('You haven\'t chosen an operation modus!')
err5  = err.format('You haven\'t chosen a workflow type!')
err6  = err.format('We haven\'t been able to retrieve the citation information with the provided identifier. Please check your DOI!')
err7  = err.format('Please, check the question \'Is the model already deposited in MaRDI Knowledge Graph or Wikidata?\'. Your mardi:QID or wikidata:QID is wrong!')
err8  = err.format('Please, check the question \'Is the model already deposited in MaRDI Knowledge Graph or Wikidata?\'. You haven\'t answered the question!')
err9  = err.format('A new model requires a main subject!')
err10 = err.format('For workflow finding via research objective or input data use string instead of QIDs.')
err11 = err.format('Please, check the question \'Provide an ID for the method.\'. The mardi:QID or wikidata:QID you provided in set {} does not exist!')
err12 = err.format('Please, check the question \'Provide an ID for the software.\'. The mardi:QID or wikidata:QID you provided in set {} does not exist!')
err13 = err.format('Please, check the question \'Provide an ID for the Input Data\'. The mardi:QID or wikidata:QID you provided in set {} does not exist!')
err14 = err.format('Please, check the question \'Provide an ID for the Output Data\'. The mardi:QID or wikidata:QID you provided in set {} does not exist!')
err15 = err.format('A new workflow needs to be related to scientific disciplines!')
err16 = err.format('A new software (set {}) requires a programming language!')
err17 = err.format('A new method (set {}) requires a main subject!')
err18 = err.format('A workflow with the same label and description already exists on the MaRDI Portal!')
err19 = err.format('You don\'t have permission to write to the MaRDI Portal. Check your bot credentials.')
err20 = err.format('Please, provide a research objective!')
err21 = err.format('A new model requires name and description!')
err22 = err.format('A new method (set {}) requires name and description!')
err23 = err.format('A new software (set {}) requires name and description!')
err24 = err.format('A new input data set (set {}) requires a name!')
err25 = err.format('A new output data set (set {}) requires a name!')

# HTML stuff to preview Documentation

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



