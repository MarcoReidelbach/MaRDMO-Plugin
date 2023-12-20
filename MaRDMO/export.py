import pypandoc
import re
import requests

from django.http import HttpResponse

from rdmo.projects.exports import Export
from rdmo.views.utils import ProjectWrapper
from rdmo.views.templatetags import view_tags

from wikibaseintegrator import wbi_login, WikibaseIntegrator
from wikibaseintegrator.datatypes import ExternalID, Item, String, Time, MonolingualText
from wikibaseintegrator.wbi_enums import ActionIfExists
from wikibaseintegrator.wbi_config import config as wbi_config

from .para import *
from .config import *
from .citation import *
from .id import *
from .sparql import *
from .display import *

try:
    # Get login credentials if available 
    from config.settings import lgname, lgpassword
except:
    lgname=''
    lgpassword=''

class MaRDIExport(Export):

    def render(self):
        '''Function that renders User answers to MaRDI template
           (adjusted from csv export)'''
 
### Check if MaRDI Questionaire is used ###########################################################################################################################################################
        if str(self.project.catalog)[-5:] != 'MaRDI':
            return HttpResponse(response_temp.format(err1).format(self.project.catalog))
        
### Gather all User Answers in Dictionary (modified RDMO Code) ####################################################################################################################################

        project_wrapper = ProjectWrapper(self.project, self.snapshot)
        
        data = {}
        for question in project_wrapper.questions:
            set_prefixes = view_tags.get_set_prefixes({}, question['attribute'], project=project_wrapper)
            for set_prefix in set_prefixes:
                set_indexes = view_tags.get_set_indexes({}, question['attribute'], set_prefix=set_prefix,
                                                        project=project_wrapper)
                for set_index in set_indexes:
                    values = view_tags.get_values(
                        {}, question['attribute'], set_prefix=set_prefix, set_index=set_index, project=project_wrapper)
                
                    labels = view_tags.get_labels(
                        {}, question, set_prefix=set_prefix, set_index=set_index, project=project_wrapper)
                
                    result = view_tags.check_element(
                        {}, question, set_prefix=set_prefix, set_index=set_index, project=project_wrapper)

                    if labels:
                        data[question['attribute']+'_'+str(set_index)]=self.stringify_values(values)
                    else:
                        data[question['attribute']+'_0']=self.stringify_values(values)


       ###################################################################################################################################################
       ###################################################################################################################################################
       ##                                                                                                                                               ##
       ##                                                                                                                                               ##
       ##    ░█──░█ ░█▀▀▀█ ░█▀▀█ ░█─▄▀ ░█▀▀▀ ░█─── ░█▀▀▀█ ░█──░█ 　 ░█▀▀▄ ░█▀▀▀█ ░█▀▀█ ░█─░█ ░█▀▄▀█ ░█▀▀▀ ░█▄─░█ ▀▀█▀▀ ─█▀▀█ ▀▀█▀▀ ▀█▀ ░█▀▀▀█ ░█▄─░█    ##
       ##    ░█░█░█ ░█──░█ ░█▄▄▀ ░█▀▄─ ░█▀▀▀ ░█─── ░█──░█ ░█░█░█ 　 ░█─░█ ░█──░█ ░█─── ░█─░█ ░█░█░█ ░█▀▀▀ ░█░█░█ ─░█── ░█▄▄█ ─░█── ░█─ ░█──░█ ░█░█░█    ##
       ##    ░█▄▀▄█ ░█▄▄▄█ ░█─░█ ░█─░█ ░█─── ░█▄▄█ ░█▄▄▄█ ░█▄▀▄█ 　 ░█▄▄▀ ░█▄▄▄█ ░█▄▄█ ─▀▄▄▀ ░█──░█ ░█▄▄▄ ░█──▀█ ─░█── ░█─░█ ─░█── ▄█▄ ░█▄▄▄█ ░█──▀█    ##
       ##                                                                                                                                               ##
       ##                                                                                                                                               ##
       ###################################################################################################################################################
       ###################################################################################################################################################

        
        # If Workflow Documentation wanted
        if data[dec[0][0]] in (dec[0][1],dec[0][2]):


### Checks for Workflow Documentation #############################################################################################################################################################

            # Login Credentials for MaRDI Portal Export
            if data[dec[2][0]] == dec[2][2] and data[dec[3][0]] in (dec[3][1],dec[3][2]):
                if not (lgname and lgpassword):
                    #Stop if no Login Credentials are provided
                    return HttpResponse(response_temp.format(err19))

            # Research Objective Provided
            res_obj=self.wikibase_answers(data,ws['obj'])[0] 
            if not res_obj:
                # Stop if no Research Objective is provided
                return HttpResponse(response_temp.format(err20))
            
            # Workflow Type (THEO/EXP)
            if data[dec[1][0]] not in (dec[1][1],dec[1][2],dec[1][3],dec[1][4]):
                # Stop if no Workflow Type is chosen
                return HttpResponse(response_temp.format(err5))
            
            # Identical Workflow on MaRDI Portal
            if data[dec[2][0]] == dec[2][2] and data[dec[3][0]] in (dec[3][1],dec[3][2]):
                if self.get_results(mardi_endpoint,mini.format('?qid',mbody.format(self.project.title.replace("'",r"\'"),res_obj.replace("'",r"\'"))))[0]:
                    # Stop if Workflow with similar Label and Description on MaRDI Portal
                    return HttpResponse(response_temp.format(err18))
                
### Get Paper Information provided by User ########################################################################################################################################################

            paper=self.wikibase_answers(data,ws['doi'])[0]

### MaRDI KG and Wikidata Queries #################################################################################################################################################################

            # Initialize dictionaries for MaRDI KG (mq) and Wikidata (wq) queries
            wq = {}
            mq = {}

            # If Portal integration wanted, get further publication information
            if data[dec[2][0]] == dec[2][2] and data[dec[3][0]] in (dec[3][1],dec[3][2]):
                # Extract Paper DOI
                doi=re.split(':',paper)
                
                if doi[0] == 'Yes':
                    
                    if not doi[-1]:
                        # Stop if no DOI provided
                        return HttpResponse(response_temp.format(err6))
                
                    # Get Citation and Author Information
                    orcid,string,cit=GetCitation(doi[-1])
                    
                    if not cit:
                        # Stop if no Information available via DOI
                        return HttpResponse(response_temp.format(err6))

                    # Query Wikidata and MaRDI KG by all User Answers and Citation Information 
                    wq, mq = self.sparql(data,ws,orcid,doi,cit)

### Checkout Paper via DOI ########################################################################################################################################################################

                    if mq['mqpub']["qid_doi"]["value"]:
                        # If Paper with DOI on MaRDI Portal store QID
                        paper_qid=mq['mqpub']["qid_doi"]["value"]

                    else:

                        # If no Paper with DOI on MaRDI Portal, check if Paper with DOI on Wikidata
                        if wq['wqpub']["qid_doi"]["value"]:

                            # If on Wikidata check if Paper with same label and description is on MaRDI Portal
                            if mq['mqpub']["qid_ch1"]["value"]:
                                # If Paper exists on MaRDI Portal store QID.
                                paper_qid=mq['mqpub']["qid_ch1"]["value"]

                            else:
                                # If Paper only on Wikidata, generate Dummy Entry (i.e. Wikidata Label, Description, QID Mapping) and store QID. 
                                paper_qid=self.entry(wq['wqpub']["label_doi"]["value"],wq['wqpub']["quote_doi"]["value"],[(ExternalID,wq['wqpub']["qid_doi"]["value"],P2)])

                        else:

### Checkout Paper via Title ######################################################################################################################################################################

                            # If Title in Citation
                            if cit['title']:

                                if mq['mqpub']["qid_tit"]["value"]:
                                    # If Paper with Title on MaRDI Portal store QID
                                    paper_qid=mq['mqpub']["qid_tit"]["value"]

                                else:

                                    # If no Paper with Title on MaRDI Portal, check if Paper with Title on Wikidata
                                    if wq['wqpub']["qid_tit"]["value"]:
                                        # If Paper only on Wikidata, generate Dummy Entry (i.e. Wikidata Label, Description, QID Mapping) and store QID.
                                        paper_qid=self.entry(wq['wqpub']["label_tit"]["value"],wq['wqpub']["quote_tit"]["value"],[(ExternalID,wq['wqpub']["qid_tit"]["value"],P2)])

                                    else:

### Create New Publication Entry ##################################################################################################################################################################

### Add Authors of Paper with ORCID ID to MaRDI Portal ############################################################################################################################################

                                        author_qids=[]
                                        for i,aut in enumerate(orcid):
                                            # If authors not on MaRDI Portal, add them.
                                            author_qids.append(self.paper_prop_entry(wq['wqaut'+str(i)],mq['mqaut'+str(i)],[aut[0],'researcher',
                                                                                     [(Item,Q7,P4),(Item,Q8,P21),(ExternalID,aut[1],P22)]]))
                                    
### Add Language of Paper to MaRDI Portal ######################################################################################################################################################### 

                                        if cit['language']:
                                            # If language not on MaRDI Portal, add it.
                                            cit['language']=self.paper_prop_entry(wq['wqlan'],mq['mqlan'],[lang_dict[cit['language']],'language',
                                                                                  [(Item,Q11,P4)]])

### Add Journal of Paper to MaRDI Portal ##########################################################################################################################################################

                                        if cit['journal']:
                                            # If journal not in Portal, create journal entry for publication                                                     
                                            cit['journal']=self.paper_prop_entry(wq['wqjou'],mq['mqjou'],[cit['journal'],'scientific journal',
                                                                                 [(Item,Q9,P4)]])

### Create Publication Entry on MaRDI Portal #####################################################################################################################################################

                                        paper_qid=self.entry(cit['title'],'publication',[(Item,Q1 if cit['ENTRYTYPE'] == 'article' else Q10,P4)]+
                                                             [(Item,aut,P8) for aut in author_qids]+[(String,aut,P9) for aut in string]+
                                                             [(Item,cit['language'],P10),(Item,cit['journal'],P12),(MonolingualText,cit['title'],P7),
                                                              (Time,cit['pub_date']+'T00:00:00Z',P11),(String,cit['volume'],P13),(String,cit['number'],P14),
                                                              (String,cit['pages'],P15),(ExternalID,cit['doi'].upper(),P16)])  
                else:
                    # No DOI provided
                    paper_qid=[]

            if not (wq and mq):
                # Query Wikidata and MaRDI KG by all User Answers without Citation Information 
                wq, mq = self.sparql(data,ws)

### Integrate related Model in MaRDI KG ###########################################################################################################################################################

            models, data, error = self.Entry_Generator('mod','moms',                # Entry of Model (mod) with Main Subject (moms) as Subproperty
                                                       [True,True,False],           # Generation wanted, QID Generation wanted, String Generation not wanted
                                                       [Q3,P17],                    # instance of mathematical model (Q3), main subject (P17)
                                                       wq,mq,data)                  # data from wikidata (wq), MaRDI KG (mq) and user (data)
            
            if error[0] == 0:
                # Stop if no Name and Description provided for new model entry
                return HttpResponse(response_temp.format(err21.format(error[1])))

            elif error[0] == 1:
                #Stop if no main subject provided for new model entry
                return HttpResponse(response_temp.format(err9.format(error[1])))
            
### Integrate related Methods in MaRDI KG #########################################################################################################################################################

            methods, data, error = self.Entry_Generator('met','mems',               # Entry of Methods (met) with Main Subject (mems) as Subproperty
                                                        [True,True,False],          # Generation wanted, QID Generation wanted, String Generation not wanted
                                                        [Q4,P17],                   # instance of method (Q4), main subject (P17)
                                                        wq,mq,data)                 # data from wikidata (wq), MaRDI KG (mq) and user (data)

            if error[0] == 0:
                # Stop if no Name and Description provided for new method entry
                return HttpResponse(response_temp.format(err22.format(error[1])))
            
            elif error[0] == 1:
                #Stop if no main subject provided for new method entry
                return HttpResponse(response_temp.format(err17.format(error[1])))

### Integrate related Softwares in MaRDI KG #######################################################################################################################################################

            softwares, data, error = self.Entry_Generator('sof','pl',               # Entry of Softwares (sof) with Programming Languages (pl) as Subproperty
                                                          [True,True,True],         # Generation wanted, QID Generation wanted, String Generation wanted
                                                          [Q5,P19],                 # instance of software (Q5), programmed in (P19)
                                                          wq,mq,data)               # data from wikidata (wq), MaRDI KG (mq) and user (data)

            if error[0] == 0:
                # Stop if no Name and Description provided for new software entry
                return HttpResponse(response_temp.format(err23.format(error[1])))
            
            elif error[0] == 1:
                #Stop if no programming language provided for new software entry
                return HttpResponse(response_temp.format(err16.format(error[1])))
            
### Integrate related Input Data Sets in MaRDI KG #################################################################################################################################################
            
            inputs, data, error = self.Entry_Generator('inp','',                    # Entry of Input Data Sets (inp) with no Subproperty
                                                       [True,False,False],          # Generation wanted, QID Generation not wanted, String Generation not wanted
                                                       [Q6,''],                     # instance of data set (Q6)
                                                       wq,mq,data)                  # data from wikidata (wq), MaRDI KG (mq) and user (data)

            if error[0] == 0:
                # Stop if no Name and Description provided for new input data set
                return HttpResponse(response_temp.format(err24.format(error[1])))

### Integrate related Output Data Sets in MaRDI KG ################################################################################################################################################

            outputs, data, error = self.Entry_Generator('out','',                   # Entry of Output Data Sets (out) with no Subproperty
                                                        [True,False,False],         # Generation wanted, QID Generation not wanted, String Generation not wanted
                                                        [Q6,''],                    # instance of data set (Q6)
                                                        wq,mq,data)                 # data from wikidata (wq), MaRDI KG (mq) and user (data)

            if error[0] == 0:
                # Stop if no Name and Description provided for new output data set
                return HttpResponse(response_temp.format(err25.format(error[1])))

### Integrate related Disciplines in MaRDI KG #####################################################################################################################################################

            disciplines, data, error = self.Entry_Generator('dis','',               # Entry of Disciplines (dis) with no Subproperty
                                                            [False,False,False],    # Generation not wanted, QID Generation not wanted, String Generation not wanted
                                                            ['',''],                # nothing
                                                            wq,mq,data)             # data from wikidata (wq), MaRDI KG (mq) and user (data)

            if error[0] == 2:
                # Stop if no Discipline provided by User
                return HttpResponse(response_temp.format(err15.format(error[1])))
         
### Integrate Workflow in MaRDI KG ################################################################################################################################################################

            if data[dec[2][0]] == dec[2][2] and data[dec[3][0]] in (dec[3][1],dec[3][2]):
                # If MaRDI KG integration is desired
                workflow_qid=self.entry(self.project.title, res_obj,                                       # Name (self.project.title) and Description (res_obj) of Workflow
                                        [(Item,Q2,P4),                                                     # instance of (P4) research workflow (Q2)
                                         (Item,paper_qid,P3)]+                                             # cites work (P3) paper (paper_qid) provided by user
                                        [(Item,discipline,P5) for discipline in disciplines]+              # field of work (P5) disciplines (discipline) provided by user
                                        [(Item,i,P6) for i in models+methods+softwares+inputs+outputs])    # uses (P6) models, methods, softwares, inputs, outputs
            
### Generate Workflow Page ########################################################################################################################################################################

            # Create Template with Tables
            temp=self.dyn_template(data)
                      
            # Fill out MaRDI Template
            for entry in data.items():
                temp=re.sub('"','',re.sub(";","<br/>",re.sub("Yes: |'","",re.sub(entry[0],repr(entry[1]),temp))))
        
            # Refine completed Template
            for refine_str in refine_strs:
                temp=re.sub(refine_str, "", temp)

### Publish Workflow Page #########################################################################################################################################################################

            if data[dec[2][0]] == dec[2][1]: 
                # Download as Markdown
                response = HttpResponse(temp, content_type="application/md")
                response['Content-Disposition'] = 'filename="workflow.md"'
                return response
            
            elif data[dec[2][0]] == dec[2][2] and data[dec[3][0]] not in (dec[3][1],dec[3][2]):
                # Preview Markdown as HTML
                return HttpResponse(html.format(pypandoc.convert_text(temp,'html',format='md')))
            
            elif data[dec[2][0]] == dec[2][2] and data[dec[3][0]] in (dec[3][1],dec[3][2]):

                # Convert to Mediawiki Format
                page = re.sub('{\|','{| class="wikitable"',pypandoc.convert_text(temp,'mediawiki',format='md'))
               
               # Insert Links for MaRDI, wikidata, swmath and doi entities 
                for linker in linkers:
                    page = re.sub(r'{0}({1})'.format(linker[0],linker[1]), r'{0}[{1}\1 \1]'.format(linker[0],linker[2]), page)

                # Export Page to MaRDI Portal
                self.wikipage_export(self.project.title,page)
               
               # Successful Export to Portal
                return HttpResponse(done.format(export.format(mardi_wiki+self.project.title.replace(' ','_'),mardi_wiki+'Item:'+workflow_qid)))
            
            else:
                # Stop if no Export Type is chosen
                return HttpResponse(response_temp.format(err2))


       ######################################################################################################
       ######################################################################################################
       ##                                                                                                  ##
       ##                                                                                                  ##
       ##    ▒█░░▒█ ▒█▀▀▀█ ▒█▀▀█ ▒█░▄▀ ▒█▀▀▀ ▒█░░░ ▒█▀▀▀█ ▒█░░▒█ 　 ▒█▀▀▀█ ▒█▀▀▀ ░█▀▀█ ▒█▀▀█ ▒█▀▀█ ▒█░▒█   ##
       ##    ▒█▒█▒█ ▒█░░▒█ ▒█▄▄▀ ▒█▀▄░ ▒█▀▀▀ ▒█░░░ ▒█░░▒█ ▒█▒█▒█ 　 ░▀▀▀▄▄ ▒█▀▀▀ ▒█▄▄█ ▒█▄▄▀ ▒█░░░ ▒█▀▀█   ##
       ##    ▒█▄▀▄█ ▒█▄▄▄█ ▒█░▒█ ▒█░▒█ ▒█░░░ ▒█▄▄█ ▒█▄▄▄█ ▒█▄▀▄█ 　 ▒█▄▄▄█ ▒█▄▄▄ ▒█░▒█ ▒█░▒█ ▒█▄▄█ ▒█░▒█   ##
       ##                                                                                                  ##
       ##                                                                                                  ##
       ######################################################################################################
       ######################################################################################################


        # If Workflow Search wanted
        elif data[dec[0][0]] in (dec[0][3],dec[0][4]):

            # Key Word and Entities to filter Workflows
            search_objs=self.wikibase_answers(data,ws['sea'])

### SPARQL via Research Objectives ################################################################################################################################################################
            
            # SPARQL string definitions
            quote_str = ''
            res_obj_strs = ''

            # If SPARQL query via research objective desired
            if data[dec[4][0]] in (dec[4][1],dec[4][2]):
                # Get description of workflow
                quote_str = quote_sparql
                # Separate key words for SPARQL query vie research objective
                res_objs=search_objs[0].split('; ')
                if res_objs:
                    # Define Filters for SPARQL queries
                    for res_obj in res_objs:
                        res_obj_strs+=res_obj_sparql.format(res_obj.lower())

### SPARQL via Research Disciplines ###############################################################################################################################################################

            # SPARQL string definitions
            res_disc_str = ''

            # If SPARQL query via research discipline desired
            if data[dec[5][0]] in (dec[5][1],dec[5][2]):
                # Separate disciplines for SPARQL query via research discipline 
                res_discs=search_objs[1].split('; ')
                if res_discs:
                    for res_disc in res_discs:
                        # Get ID of research discipline
                        res_disc_id = res_disc.split('<|>')[0].split(':')[1]
                        # Define Filters for SPARQL queries
                        res_disc_str += res_disc_sparql.format(P5,res_disc_id)

### SPARQL via Mathematical Models, Methods, Softwares, Input or Output Data Sets #################################################################################################################

            # SPARQL string definitions
            mmsios_str = ''

            # If SPARQL query via Mathematical Models, Methods, Softwares, Input or Output Data Sets
            if data[dec[6][0]] in (dec[6][1],dec[6][2]):
                # Separate Mathematical Model, Methods, Software, Input or Output Data Sets
                mmsios=search_objs[2].split('; ')
                if mmsios:
                    for mmsio in mmsios:
                        # Get ID of mathematical model, method, software, input or output data set
                        mmsio_id = mmsio.split('<|>')[0].split(':')[1]
                        # Define Filters for SPARQL queries
                        mmsios_str += mmsio_sparql.format(P6,mmsio_id)

### Set up Query, query MaRDI Portal and return Results ###########################################################################################################################################

            # Set up entire SPARQL query
            query = query_base.format(P4,Q2,res_disc_str,mmsios_str,quote_str,res_obj_strs)
            
            # Query MaRDI Portal
            results = self.get_results(mardi_endpoint, query)

            # Number of Results
            no_results = str(len(results))
            
            # Generate Links to Wikipage and Knowledge Graoh Entry of Results
            links =''
            for result in results:
                links+=link.format(result["label"]["value"],mardi_wiki+result["label"]["value"].replace(' ','_'),mardi_wiki+'Item:'+result["qid"]["value"])

            return HttpResponse(search_done.format(no_results,links))
 
        
        else:
            # Stop if Workflow Documentation or Search not chosen
            return HttpResponse(response_temp.format(err4))

    def stringify_values(self, values):
        '''Original function from csv export'''
        if values is not None:
            return '; '.join([self.stringify(value['value_and_unit']) for value in values])
        else:
            return ''

    def stringify(self, el):
        '''Original function from csv export'''
        if el is None:
            return ''
        else:
            return re.sub(r'\s+', ' ', str(el))

    def create_table(self, column_topics, row_ids, rows):
        '''Function that creates a markdwon table with headers.
           Row number depends on user answers, dummy entries''' 
        table=''
        for row in range(rows):
            table=table+'| '
            for n,topic in enumerate(column_topics):
                if row==0:
                    table=table+topic+' | '
                elif row==1:
                    table=table+'-- | '
                else:
                    table=table+row_ids[n]+'_'+str(row-2)+' | '
            table=table+'\n'
        return table

    def dyn_template(self, data):
        '''Function that chooses proper raw MaRDI template and
           inserts appropriate tables depending on user answers.'''
        if data[dec[1][0]] in (dec[1][1],dec[1][2]):
            # Theoretical workflow properties
            temp=math_temp
            tables=math_tables
            topics=math_topics
            ids=math_ids
        elif data[dec[1][0]] in (dec[1][3],dec[1][4]):
            # Experimental Workflow properties
            temp=exp_temp
            tables=exp_tables
            topics=exp_topics
            ids=exp_ids
        else:
            temp=[]
            return temp
       
        # Set up involved discipines
        temp=re.sub('DISCIPLINES','; '.join([key for key in data.keys() if ws['dis'][0]+'_' in key]),temp)

        # Set up tables through set numbers (n_max)
        for n,table in enumerate(tables):
            n_max=max([int(x.split('_')[-1]) if y in x else 0 for x in data.keys() for y in ids[n]])+1
            t=self.create_table(topics[n],ids[n],n_max+2)
            temp=re.sub(table,t,temp)
        return(temp)
       
    def wikipage_export(self,title,content): 
        '''Genereic Mediawiki Example'''

        S = requests.Session()

        URL = mardi_api

        # Step 1: GET request to fetch login token
        PARAMS_0 = {
            "action": "query",
            "meta": "tokens",
            "type": "login",
            "format": "json"
        }

        R = S.get(url=URL, params=PARAMS_0)
        DATA = R.json()
        
        LOGIN_TOKEN = DATA['query']['tokens']['logintoken']

        # Step 2: POST request to log in.
        PARAMS_1 = {
            "action": "login",
            "lgname": lgname,
            "lgpassword": lgpassword,
            "lgtoken": LOGIN_TOKEN,
            "format": "json"
        }

        R = S.post(URL, data=PARAMS_1)

        # Step 3: GET request to fetch CSRF token
        PARAMS_2 = {
            "action": "query",
            "meta": "tokens",
            "format": "json"
        }

        R = S.get(url=URL, params=PARAMS_2)
        DATA = R.json()

        CSRF_TOKEN = DATA['query']['tokens']['csrftoken']

        # Step 4: POST request to edit a page

        post_content=re.sub('<math display="block">','<math>',content)

        PARAMS_3 = {
            "action": "edit",
            "title": title,
            "token": CSRF_TOKEN,
            "format": "json",
            "appendtext": post_content
            }

        R = S.post(URL , data=PARAMS_3, files=dict(foo='bar'))
        return

    def set_lengths(self, data):
        '''Get length of the User sets'''
        length=[]
        sts=['Section_3/Set_1','Section_4/Set_2','Section_4/Set_3','Section_4/Set_6','Section_4/Set_7']
        for st in sts:
            i=0
            data_filter = dict(filter(lambda item: st in item[0], data.items()))
            for key in data_filter.keys():
                if int(key.split('_')[-1])>=i:
                    i=int(key.split('_')[-1])+1
            length.append(i)
        return length

    def wikibase_answers(self, data, wiki, length=-1):
        '''Takes data and extracts answers relevant for Wiki'''
        wiki_answers=[]
        if length >= 0:
            for question in wiki:
                for idx in range(length):
                    if question+'_'+str(idx) in data:
                        wiki_answers.append(data[question+'_'+str(idx)])
                    else:
                        wiki_answers.append('')
        else:
            for question in wiki:
                if question in data:
                    wiki_answers.append(data[question])
                else:
                    wiki_answers.append('')
        return wiki_answers

    def wikibase_login(self):
        '''Login stuff for wikibase'''
        wbi_config['MEDIAWIKI_API_URL'] = mardi_api
    
        #login_instance = wbi_login.OAuth1(consumer_token, consumer_secret, access_token, access_secret)
        login_instance = wbi_login.Login(user=lgname, password=lgpassword)

        wbi = WikibaseIntegrator(login=login_instance)

        return wbi

    def entry(self,label,description,facts):
        '''Takes arbitrary information and generates MaRDI portal entry.'''
        wbi = self.wikibase_login()
        
        item = wbi.item.new()
        item.labels.set('en', label)
        item.descriptions.set('en', description)

        data=[]
        for fact in facts:
            if fact[1]:
                if fact[0] == MonolingualText:
                    data.append(fact[0](text=fact[1],prop_nr=fact[2]))
                elif fact[0] == Time:
                    data.append(fact[0](time=fact[1],prop_nr=fact[2]))
                else:
                    data.append(fact[0](value=fact[1],prop_nr=fact[2]))
        item.claims.add(data)
            
        item.write()

        return item.id

    def get_results(self,endpoint_url, query):
        '''Perform SPARQL Queries via Get requests'''
        req=requests.get(endpoint_url, params = {'format': 'json', 'query': query}, headers = {'User-Agent': 'MaRDMO_0.1 (https://zib.de; reidelbach@zib.de)'}).json()
        return req["results"]["bindings"]
    
    def portal_wikidata_check(self,mquery,wquery,data):
        '''Function checks if an entry is on MaRDI portal and returns its QID
           or on Wikidata and copies the entry to the MaRDI portal and returns
           its QID.'''
        if wquery['qid'][0] == 'mardi':
            qid = wquery['qid'][-1]
            entry = [wquery['label'],wquery['quote']]
        elif wquery['qid'][0] == 'wikidata':
            entry = [wquery['label'],wquery['quote']]
            if mquery['qid']['value']:
                qid = mquery['qid']['value']
            else:
                #Create dummy entry and store QID if portal publication is desired
                if data[dec[2][0]] == dec[2][2] and data[dec[3][0]] in (dec[3][1],dec[3][2]):
                    #Create dummy entry and store QID
                    qid = self.entry(wquery['label'],wquery['quote'],[(ExternalID,wquery['qid'][-1],P2)])
                else:
                    qid = 'tbd'
        elif mquery['qid']['value']:
            entry = [wquery['label'],wquery['quote']]
            qid = mquery['qid']['value']
        else:
            #QID not existing
            qid = None
            entry = None

        return qid, entry
        
    def paper_prop_entry(self,wquery,mquery,props):
        '''This function takes (a property of) a paper and creates the corresponding wikibase entries.'''
        if mquery["qid"]["value"]:
            #If on Portal store QID
            qid=mquery["qid"]["value"]
        else:
            #If not on Portal, check if on Wikidata
            if wquery["qid"]["value"]:
                if mquery["qid2"]["value"]:
                    #If on Portal, store QID.
                    qid=mquery["qid2"]["value"]
                else:
                    #If only on wikidata, generate dummy entry, store QID.
                    qid=self.entry(wquery["label"]["value"],wquery["quote"]["value"],[(ExternalID,wquery["qid"]["value"],P2)])
            else:
                #If not on Portal / Wikidata create entry
                if mquery["qid3"]["value"]:
                    #If on Portal, store QID.
                    qid=mquery["qid3"]["value"]
                else:
                    #Create entry, store QID.
                    qid=self.entry(props[0],props[1],props[2])
        return qid

    def sparql(self,data,ws,orcid=None,doi=None,cit=None):
        '''This function takes user answers and performs SPARQL queries to Wikidata and MaRDI portal.'''
        
        length = self.set_lengths(data)

        types = ['model', 'method', 'software', 'inputs', 'outputs', 'disciplines']
        strings = ['mod', 'met', 'sof', 'inp', 'out', 'dis']
        strings2 = ['moms','mems','pl']

        user_answers ={}
        wq = {} ; qw = {}
        mq = {} ; qm = {}

        ### Gather all User Answers relevant for MaRDI KG

        for IDX, (TYPE, ABBR) in enumerate(zip(types, strings)):
            
            # x[0] all user answers for model, methods, software, inputs, outputs and disciplines
            # x[1] number of models, methods, softwares, inputs, outputs and disciplines
            # x[2] qid, name and description of model, methods, softwares, inputs, outputs and disciplines
            # x[3] qid, name, description of main subject of model and methods and programming languages of softwares
            # x[4] qid, name, description, main subject / programming language, formula, external id of model, methods, softwares, inputs, outputs and disciplines
            # x[5] number of main subjects of model and methods or programming languages of softwares

            x = []

            x.append(self.wikibase_answers(data, ws[ABBR], length[IDX]) if ABBR != 'dis' else self.wikibase_answers(data, ws[ABBR])[0].split('; '))
            
            x.append(length[IDX] if ABBR != 'dis' else len(x[0]) if x else 0)
            
            x.append([re.split(' <\|> ', x[0][i]) if x[0][i] else 
                     ['', x[0][x[1] + i] if ABBR in strings[:5] else '',
                      x[0][x[1] * 2 + i] if ABBR in strings[:3] else 'data set' if ABBR in strings[3:5] else ''] for i in range(x[1])])
            
            x.append([[re.split(' <\|> ', X) if X  else ['', '', '']
                      for X in x[0][i].split('; ')] for i in range(x[1] * 3, x[1] * 4)] if ABBR in strings[:3] else [])
         
            x.append([[x[2][i][j] for j in range(3)] + [x[3][i] if ABBR in strings[:3] else '',
                      x[0][x[1] * 4 + i] if ABBR in strings[:2] else '',
                      x[0][len(x[0]) - x[1] + i] if ABBR in strings[:5] else ''] for i in range(x[1])])
            
            x.append([len(s) if x and s[0][0] else 0 for s in x[3]] if ABBR in strings[:3] else 0)

            user_answers.update({TYPE: x})

        ### Number of Methods, Software, Inputs, Outputs, Disciplines entered by User
       
        wq.update({'no' : {s : user_answers[d][1] for s,d in zip(strings,types)}})
        
        ### Number of Main Subjects and Programming Languages entered by User
       
        for s,d in zip(strings2,types[:3]):
            wq.update({s+str(i) : {'no' : j} for i,j in enumerate(user_answers[d][5])})
        
        ### Wikidata Infos (wq) and MaRDI KG SPARQL Queries (mq) for Model, Method, Software, Input, Output, Discipline
       
        for s,d in zip(strings,types):

            wq.update({'wq'+s+str(i): {'qid':m[0].split(':'), 'label':m[1], 'quote':m[2], 'form':m[4], 'id':m[5]} for i,m in enumerate(user_answers[d][4])})
            
            qm.update({'mq'+s+str(i) : mini.format('?qid',mbody.format(wq['wq'+s+str(i)]['label'].replace("'",r"\'"),
                                                                       wq['wq'+s+str(i)]["quote"].replace("'",r"\'")))
                                                                       for i in range(user_answers[d][1])})

            if s in strings[:3]:

                wq.update({'wq'+s+'_sub'+str(i)+'_'+str(j): {'qid': f[0].split(':'), 'label':f[1], 'quote':f[2]} for i,ss in enumerate(user_answers[d][4]) for j,f in enumerate(ss[3])})

                qm.update({'mq'+s+'_sub'+str(i)+'_'+str(j) : mini.format('?qid',mbody.format(wq['wq'+s+'_sub'+str(i)+'_'+str(j)]['label'].replace("'",r"\'"),
                                                                                             wq['wq'+s+'_sub'+str(i)+'_'+str(j)]['quote'].replace("'",r"\'")))
                                                                                             for i,ss in enumerate(user_answers[d][4]) for j,_ in enumerate(ss[3])})

        ### Request Data from MaRDI KG

        for key in qm.keys():
            mq.update({key:{**dict.fromkeys({'qid'},{'value':''}),**self.get_results(mardi_endpoint,qm[key])[0]}})
        
        ### Additional Queries if Publication is provided

        if cit:
            
            #Generate Keys for Publication queries

            keys = dict(Keys)
            key_dat=[orcid]
            key_ind=['pub']

            for inds in zip(key_dat,key_ind):
                for i,_ in enumerate(inds[0]):
                    if type(keys_flex['wq'+inds[1]]) == str:
                        keys['wq'+inds[1]]+=keys_flex['wq'+inds[1]].format(i)
                        keys['mq'+inds[1]]+=keys_flex['mq'+inds[1]].format(i)
                    else:
                        keys['wq'+inds[1]]+=keys_flex['wq'+inds[1]][0].format(i)
                        keys['mq'+inds[1]]+=keys_flex['mq'+inds[1]][0].format(i)

            #Set up SPRQL query and request data from wikidata

            qw.update({'wqpub' : wini.format(keys['wqpub'],wbpub.format(doi[-1].upper(),cit['journal'].lower(),lang_dict[cit['language']],
                                    cit['language'],cit['title'],''.join([''.join(wbaut.format(i,aut[1])) for i,aut in enumerate(orcid)])))})
            
            wq.update({'wqpub':{**dict.fromkeys(keys['wqpub'].split(' ?'),{"value":''}),**self.get_results(wikidata_endpoint,qw['wqpub'])[0]}})

            #Set up SPARQL query and request data from MaRDI KG
            
            qm.update({'mqpub' : mini.format(keys['mqpub'],mbpub.format(doi[-1].upper(),wq['wqpub']["label_doi"]["value"],wq['wqpub']["quote_doi"]["value"],cit['journal'].lower(),
                                    wq['wqpub']["label_jou"]["value"],wq['wqpub']["quote_jou"]["value"],lang_dict[cit['language']],cit['language'],
                                    wq['wqpub']["label_lan"]["value"],wq['wqpub']["quote_lan"]["value"],cit['title'],''.join([''.join(mbaut.format(i,aut[1],
                                    wq['wqpub']['label_'+str(i)]['value'],wq['wqpub']['quote_'+str(i)]['value'],aut[0])) for i,aut in enumerate(orcid)])))})
            
            mq.update({'mqpub':{**dict.fromkeys(keys['mqpub'].split(' ?'),{"value":''}),**self.get_results(mardi_endpoint,qm['mqpub'])[0]}})
            
            #Separate author, language and journal data requested from Wikidata and MaRDI KG
            
            EXT=(['aut','_',orcid],
                 ['lan','_lan'],
                 ['jou','_jou'])

            for ext in EXT:
                if len(ext) == 2:
                    wq.update({'wq'+ext[0]:{key.split('_')[0]: value for (key, value) in wq['wqpub'].items() if ext[1] in key}})
                    mq.update({'mq'+ext[0]:{key.split('_')[0]: value for (key, value) in mq['mqpub'].items() if ext[1] in key}})
                else:
                    for i,_ in enumerate(ext[2]):
                        wq.update({'wq'+ext[0]+str(i):{key.split('_')[0]: value for (key, value) in wq['wqpub'].items() if ext[1]+str(i) in key}})
                        mq.update({'mq'+ext[0]+str(i):{key.split('_')[0]: value for (key, value) in mq['mqpub'].items() if ext[1]+str(i) in key}})

        return wq, mq

    def Entry_Generator(self,Type,Sub_Type,Generate,Relations,wq,mq,data):
        '''Function queries Wikidata/MaRDI KG, uses and generates entries in MaRDI Knowledge Graph.'''
    
        try:
            del data[ws[Type][0]]
        except:
            pass
    
        qids=[]
        for i in range(wq['no'][Type]):
    
            # Check if on Portal or in Wikidata, integrate Wikidata entry if desired
            qid,entry=self.portal_wikidata_check(mq['mq'+Type+str(i)],wq['wq'+Type+str(i)],data)
         
            # Update User answers
            if entry and qid:
                qids.append(qid)
                if Type == 'dis':
                    data.update({ws[Type][0]+'_'+str(i):entry[0]})
                else:
                    data.update({ws[Type][0]+'_'+str(i):'mardi:'+qid,ws[Type][1]+'_'+str(i):entry[0],ws[Type][2]+'_'+str(i):entry[1]})
    
            if Generate[0]:
                # Stop if no label and quote is provided for entry to generate
                if not (qid or wq['wq'+Type+str(i)]['label'] and wq['wq'+Type+str(i)]['quote']):
                    return qids, data, [0,i]
    
                # Get subproperty of 'new' entity
                sub_qids=[]
                sub_qid_str=''
    
                if Generate[1]:
                    for j in range(wq[Sub_Type+str(i)]['no']):
    
                        # Check if subproperty on Portal or in Wikidata (store QID and string)
                        if wq['wq'+Type+'_sub'+str(i)+'_'+str(j)]['qid'][0]:
                            sub_qid,entry=self.portal_wikidata_check(mq['mq'+Type+'_sub'+str(i)+'_'+str(j)],wq['wq'+Type+'_sub'+str(i)+'_'+str(j)],data)
                            sub_qids.append(sub_qid)
                            sub_qid_str+=data[ws[Type][3]+'_'+str(i)].split('; ')[j].split(' <|> ')[1]+' (mardi:'+sub_qid+');'
                     
                    # Stop if entry has no QID and its subproperty has no QID    
                    if not (qid or sub_qids):
                        return qids, data, [1,i]
    
                    if Generate[2]:
                        # Update User answers
                        data.update({ws[Type][3]+'_'+str(i):sub_qid_str})
    
                # Generate Entry QID
                if not qid:
                    # If desired generate Entry in MaRDI KG and update User answers
                    if data[dec[2][0]] == dec[2][2] and data[dec[3][0]] in (dec[3][1],dec[3][2]):
                        qids.append(self.entry(wq['wq'+Type+str(i)]['label'],wq['wq'+Type+str(i)]['quote'], 
                                               [(Item,Relations[0],P4)]+
                                               [(Item,sub_qid,Relations[1]) for sub_qid in sub_qids]+
                                               [(String,re.sub("\$","",form.lstrip()),P18) for form in re.split(';',wq['wq'+Type+str(i)]['form'])]+
                                               [(ExternalID,wq['wq'+Type+str(i)]['id'].split(':')[-1] if wq['wq'+Type+str(i)]['id'].split(':')[-1] else '',
                                                   P16 if wq['wq'+Type+str(i)]['id'].split(':')[0] == 'doi' else P20)]))
                        data.update({ws[Type][0]+'_'+str(i):'mardi:'+qids[-1]})
                    else:
                        data.update({ws[Type][0]+'_'+str(i):'mardi:tbd'})
            else:
                if not qid:
                    return qids, data, [2,i]

        return qids, data, [-1,-1]

