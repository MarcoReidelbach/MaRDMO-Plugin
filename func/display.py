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

export='''<p style="color:blue;font-size:30px;">You're Workflow has been added to the local Knowledge Graph.</p>
<p style="color:blue;font-size:30px;">See you soon on the MaRDI Portal!</p>'''

err='''<p style="color:red;font-size:50px;">Ooops...</p>
<p style="color:red;font-size:50px;">{}</p>'''

err1  = err.format('The Questionnaire \'{}\' is not suitable for the MaRDI Export!')
err2  = err.format('You haven\'t chosen an export type!')
err3  = err.format('You haven\'t chosen an entity to search for!')
err4  = err.format('You haven\'t chosen an operation modus!')
err5  = err.format('You haven\'t chosen an workflow type!')
err6  = err.format('We haven\'t been able to retrieve the citation information with the provided identifier. Please check your DOI!')
err7  = err.format('Please, check the question \'Is the model already deposited in MaRDI Knowledge Graph or Wikidata?\'. Your mardi:QID or wikidata:QID is wrong!')
err8  = err.format('Please, check the question \'Is the model already deposited in MaRDI Knowledge Graph or Wikidata?\'. You haven\'t answered the question!')
err9  = err.format('A new model requires a main subject!')
err10 = err.format('For workflow finding via research objective or input data use string instead of QIDs.')
err11 = err.format('Please, check the question \'Provide an ID for the method.\'. The mardi:QID or wikidata:QID you provided in set {} does not exist!')
err12 = err.format('Please, check the question \'Provide an ID for the software.\'. The mardi:QID or wikidata:QID you provided in set {} does not exist!')
err13 = err.format('Please, check the question \'Provide an ID for the Input Data\'. The mardi:QID or wikidata:QID you provided in set {} does not exist!')
err14 = err.format('Please, check the question \'Provide an ID for the Output Data\'. The mardi:QID or wikidata:QID you provided in set {} does not exist!')
err15 = err.format('Please, check the question \'Which disciplines can your workflow be assigned to?\'. The mardi:QID(s) or wikidata:QID(s) you provided does not exist!')
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




