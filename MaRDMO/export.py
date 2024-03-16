import pypandoc
import re
import requests

from django.http import HttpResponse
from django.shortcuts import redirect, render, reverse
from django.utils.translation import gettext_lazy as _

from rdmo.projects.exports import Export
from rdmo.views.utils import ProjectWrapper
from rdmo.views.templatetags import view_tags
from rdmo.domain.models import Attribute

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
from .handlers import *
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
                # Get user-defined Workflow Author Name and ID(s)
                user_name = self.get_answer('http://example.com/terms/domain/MaRDI/Section_0/Set_1/Question_02')
                user_ids = self.get_answer('http://example.com/terms/domain/MaRDI/Section_0/Set_1/Question_03')
                if not user_name:
                    # Stop if no Workflow Author Name provided
                    return HttpResponse(response_temp.format(err28))
                if user_ids:
                    # If ID(s) provided, check if they match the author ID(s) on MaRDI Portal. If yes, allow edits.
                    creator_orcid_id = []; creator_zbmath_id = []
                    orcid_creator = []; zbmath_creator = []
                    for user_id in user_ids:
                        user_id = user_id.split(':')
                        if user_id[0] == 'orcid':
                            creator_orcid_id.append(user_id[1])
                            orcid_creator.extend([[user_name[0],user_id[1]]])
                        elif user_id[0] == 'zbmath':
                            creator_zbmath_id.append(user_id[1])
                            zbmath_creator.extend([[user_name[0], user_id[1]]])
                        else:
                            # Stop if wrong ID type provided for Workflow author
                            return HttpResponse(response_temp.format(err27))
                else:
                    # Stop if no ID(s) provided
                    return HttpResponse(response_temp.format(err29))
                # Check if Workflow with same Label and Description on MaRDI Portal, get workflow author credntials
                req = self.get_results(mardi_endpoint,mini.format('?qid ?orcid ?zbmath',mbody2.format(self.project.title.replace("'",r"\'"),res_obj.replace("'",r"\'"),P8,P22,P23),'1'))[0]
                existing_workflow_qid = None
                if req.get('qid', {}).get('value'):
                    # Store Workflow QID and Workflow Author  credentials
                    existing_workflow_qid = req['qid']['value']
                    workflow_author_orcid = req.get('orcid', {}).get('value')
                    workflow_author_zbmath = req.get('zbmath', {}).get('value')
                    if user_ids:
                        # If ID(s) provided, check if they match the author ID(s) on MaRDI Portal. If yes, allow edits.
                        edit_allowed = True
                        for user_id in user_ids:
                            user_id = user_id.split(':')
                            if user_id[0] == 'orcid': 
                                if workflow_author_orcid:
                                    if user_id[1] == workflow_author_orcid:
                                        edit_allowed *= True
                                    else:
                                        edit_allowed *= False
                            elif user_id[0] == 'zbmath': 
                                if workflow_author_zbmath:
                                    if user_id[1] == workflow_author_zbmath:
                                        edit_allowed *= True
                                    else:
                                        edit_allowed *= False
                            else:
                                edit_allowed *= False
                    if not edit_allowed:
                        # Stop if Workflow with similar Label and Description on MaRDI Portal and edit is not allowed
                        return HttpResponse(response_temp.format(err18))
            else:
                creator_orcid_id = ''; orcid_creator = ''
                creator_zbmath_id = ''; zbmath_creator = ''

### Get Publication Information provided by User ##################################################################################################################################################

            pub_info = {}

            pub_properties = ['paper', 'all_authors', 'publication', 'entrytype', 'title', 'authors',
                              'languages' , 'journals', 'volume', 'issue', 'pages' ,'date']
            
            for pub_property, pub_id in zip(pub_properties, pub_ids):
                pub_info[pub_property] = self.get_answer(pub_id) if self.get_answer(pub_id) != ['NONE'] else ['']
              
### If Portal Integration desired, check if Paper already exists on MaRDI Portal or Wikidata  #####################################################################################################

            # If Portal integration wanted, get further publication information
            if data[dec[2][0]] == dec[2][2] and data[dec[3][0]] in (dec[3][1],dec[3][2]):
                
                # Extract Paper DOI
                doi=re.split(':', pub_info['paper'][-1])
                             
                if pub_info['paper'][0] == 'Yes':
                    
                    if not doi[-1]:
                        # Stop if no DOI provided
                        return HttpResponse(response_temp.format(err6))

                    if not pub_info['publication']:
                        # Stop if no Information available via DOI
                        return HttpResponse(response_temp.format(err6)) 
                    
                    # Get Publication ID, Label and Description
                    pub_info['publication'] = pub_info['publication'][0].split(' <|> ')
                    
                    if re.match(r"mardi:Q[0-9]+", pub_info['publication'][0]):
                        # If Paper with DOI on MaRDI Portal store QID
                        paper_qid= pub_info['publication'][0].split(':')[1]

                    elif re.match(r"wikidata:Q[0-9]+", pub_info['publication'][0]): 
                        # If Paper with DOI on Wikidata, generate dummy entry  store QID
                        paper_qid= self.entry(pub_info['publication'][1], pub_info['publication'][2], [(ExternalID, pub_info['publication'][0].split(':')[1], P2)])

                    else:
                        
### Create New Publication Entry ##################################################################################################################################################################

### Prepare User edited Authors  ##################################################################################################################################################################
                        
                        orcid_ids = []
                        orcid_authors = []
                        zbmath_ids = []
                        zbmath_authors = []
                        authors_remove = []
                        
                        # Identify Authors with ID added by User

                        other_authors = pub_info['all_authors'][len(pub_info['authors']):]

                        for author in other_authors:
                            try:
                                author_ids = re.search('\((.*)\)',author).group(1)
                            except:
                                author_ids = ''
                            
                            for author_id in author_ids.split('; '):
                                if author_id.split(':')[0] == 'orcid':
                                    orcid_ids.append(author_id.split(':')[1])
                                    orcid_authors.append([author.split(' (')[0],author_id.split(':')[1]])
                                    authors_remove.append(author)
                                elif author_id.split(':')[0] == 'zbmath':
                                    zbmath_ids.append(author_id.split(':')[1])
                                    zbmath_authors.append([author.split(' (')[0],author_id.split(':')[1]])
                                    authors_remove.append(author)
                        
                        # Remove Authors with ID added by User from non-ID Author List
                        for author in authors_remove:
                            try:
                                other_authors.remove(author)
                            except ValueError:
                                pass
                         
                        author_dict_merged = Author_Search(orcid_ids, zbmath_ids, orcid_authors, zbmath_authors)

                        # Store Publication Authors from Citation via ORCID and zbMath
                        
                        for author_id, author_data in author_dict_merged.items():
                            if author_data['mardiQID']:
                                pub_info['authors'].append('mardi:{0}'.format(author_data['mardiQID']))
                            elif author_data['wikiQID']:
                                pub_info['authors'].append('wikidata:{0} <|> {1} <|> {2}'.format(
                                    author_data['wikiQID'],
                                    author_data['wikiLabel'],
                                    author_data['wikiDescription']))
                            else:
                                if author_data['orcid']:
                                    orcid_info = 'orcid:{0}'.format(author_data['orcid'])
                                    if author_data['zbmath']:
                                        orcid_info += '; zbmath:{0}'.format(author_data['zbmath'])
                                    pub_info['authors'].append('{0} <|> {1} <|> researcher (ORCID {2})'.format(
                                        orcid_info,
                                        author_id,
                                        author_data['orcid']))
                                elif author_data['zbmath']:
                                    pub_info['authors'].append('zbmath:{0} <|> {1} <|> researcher (zbMath {2})'.format(
                                        author_data['zbmath'],
                                        author_id,
                                        author_data['zbmath']))

### Add Authors, Language an Journal of Paper to MaRDI Portal #####################################################################################################################################

                        author_qids = self.Entry_Generator_Paper_Supplements(pub_info['authors'],
                                                                             [(Item, Q7, P4), (Item, Q8, P21)],
                                                                             True)

                        language_qids = self.Entry_Generator_Paper_Supplements(pub_info['languages'],
                                                                               [(Item, Q11, P4)],
                                                                               False)

                        journal_qids = self.Entry_Generator_Paper_Supplements(pub_info['journals'],
                                                                              [(Item, Q9, P4)],
                                                                              False)

### Add Paper to  MaRDI Portal ####################################################################################################################################################################
                         
                        paper_qid=self.entry(pub_info['publication'][1], pub_info['publication'][2], 
                                             [(Item, pub_info['entrytype'][0].split(' <|> ')[0].split(':')[1], P4)] +
                                             [(Item, author, P8) for author in author_qids] +
                                             [(String, author, P9) for author in other_authors] +
                                             [(Item,language_qids[0],P10),(Item,journal_qids[0] if journal_qids else None, P12),
                                              (MonolingualText,pub_info['title'][0],P7),(Time,pub_info['date'][0][:10]+'T00:00:00Z',P11),
                                              (String,pub_info['volume'][0],P13),(String,pub_info['issue'][0],P14),
                                              (String,pub_info['pages'][0],P15),(ExternalID,doi[-1].upper(),P16)])  
                else:
                    # No DOI provided
                    paper_qid=[]

### Get Information of Workflow Creator and add Information to MaRDI Portal  ######################################################################################################################
            
            creator_dict_merged = Author_Search(creator_orcid_id, creator_zbmath_id, orcid_creator, zbmath_creator)
            
            pub_info['creator'] = []
            for author_id, author_data in creator_dict_merged.items():
                if author_data['mardiQID']:
                    pub_info['creator'].append('mardi:{0}'.format(author_data['mardiQID']))
                elif author_data['wikiQID']:
                    pub_info['creator'].append('wikidata:{0} <|> {1} <|> {2}'.format(
                        author_data['wikiQID'],
                        author_data['wikiLabel'],
                        author_data['wikiDescription']))
                else:
                    if author_data['orcid']:
                        orcid_info = 'orcid:{0}'.format(author_data['orcid'])
                        if author_data['zbmath']:
                            orcid_info += '; zbmath:{0}'.format(author_data['zbmath'])
                        pub_info['creator'].append('{0} <|> {1} <|> researcher (ORCID {2})'.format(
                            orcid_info,
                            author_id,
                            author_data['orcid']))
                    elif author_data['zbmath']:
                        pub_info['creator'].append('zbmath:{0} <|> {1} <|> researcher (zbMath {2})'.format(
                            author_data['zbmath'],
                            author_id,
                            author_data['zbmath']))

            creator_qids = self.Entry_Generator_Paper_Supplements(pub_info['creator'],
                                                                 [(Item, Q7, P4), (Item, Q8, P21)],
                                                                 True)

### Query Wikidata and MaRDI KG by all User Answers for Models, Methods, Software, etc ############################################################################################################

            wq, mq = self.sparql(data,ws)
        
### Integrate related Model in MaRDI KG ###########################################################################################################################################################

            models, data, error = self.Entry_Generator('mod','moms',                # Entry of Model (mod) with Main Subject (moms) as Subproperty
                                                       [True,False,False],          # Generation wanted, QID Generation wanted, String Generation not wanted
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

### Integrate related non-mathematical Disciplines in MaRDI KG ####################################################################################################################################

            disciplines, data, error = self.Entry_Generator('dis','',               # Entry of non-mathmatical Disciplines (dis) with no Subproperty
                                                            [False,False,False],    # Generation not wanted, QID Generation not wanted, String Generation not wanted
                                                            ['',''],                # nothing
                                                            wq,mq,data)             # data from wikidata (wq), MaRDI KG (mq) and user (data)

            if error[0] == 2:
                # Stop if no Discipline provided by User
                return HttpResponse(response_temp.format(err15.format(error[1])))

### Integrate related mathematical Fields in MaRDI KG #############################################################################################################################################

            fields, data, error = self.Entry_Generator('fie','',               # Entry of mathmatical fields (fie) with no Subproperty
                                                       [False,False,False],    # Generation not wanted, QID Generation not wanted, String Generation not wanted
                                                       ['',''],                # nothing
                                                       wq,mq,data)             # data from wikidata (wq), MaRDI KG (mq) and user (data)

            if error[0] == 2:
                # Stop if no Discipline provided by User
                return HttpResponse(response_temp.format(err26.format(error[1])))

### Integrate Workflow in MaRDI KG ################################################################################################################################################################

            if data[dec[2][0]] == dec[2][2] and data[dec[3][0]] in (dec[3][1],dec[3][2]):
                # If MaRDI KG integration is desired
                if existing_workflow_qid:
                    wbi = self.wikibase_login()
                    item = wbi.item.get(existing_workflow_qid)
                    for claim in item.claims.claims:
                        item.claims.remove(claim)
                    item.write()
                    wbi = self.wikibase_login()
                    item = wbi.item.get(existing_workflow_qid)
                    facts = [(Item,Q2,P4),(Item,paper_qid,P3)]+ \
                             [(Item,discipline,P5) for discipline in disciplines]+ \
                             [(Item,field,P5) for field in fields]+ \
                             [(Item,i,P6) for i in models+methods+softwares+inputs+outputs]+ \
                             [(Item, creator, P8) for creator in creator_qids]              
                    d=[]
                    for fact in facts:
                        if fact[1]:
                            if fact[0] == MonolingualText:
                                d.append(fact[0](text=fact[1],prop_nr=fact[2]))
                            elif fact[0] == Time:
                                d.append(fact[0](time=fact[1],prop_nr=fact[2]))
                            else:
                                d.append(fact[0](value=fact[1],prop_nr=fact[2]))
                    item.claims.add(d)
                    item.write()
                    workflow_qid = item.id
                else:
                    workflow_qid=self.entry(self.project.title, res_obj,                                       # Name (self.project.title) and Description (res_obj) of Workflow
                                            [(Item,Q2,P4),                                                     # instance of (P4) research workflow (Q2)
                                             (Item,paper_qid,P3)]+                                             # cites work (P3) paper (paper_qid) provided by user
                                            [(Item,discipline,P5) for discipline in disciplines]+              # field of work (P5) disciplines (discipline) provided by user
                                            [(Item,field,P5) for field in fields]+                             # field of work (P5) mathematical fields (field) provided by user
                                            [(Item,i,P6) for i in models+methods+softwares+inputs+outputs]+    # uses (P6) models, methods, softwares, inputs, outputs
                                            [(Item, creator, P8) for creator in creator_qids])                 # documentation authored by creator
            
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
       
        # Set up involved discipines & fields
        temp=re.sub('DISCIPLINES','; '.join([key for key in data.keys() if ws['dis'][0]+'_' in key]),temp)
        temp=re.sub('FIELDS','; '.join([key for key in data.keys() if ws['fie'][0]+'_' in key]),temp)

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
            "text": post_content
            }

        R = S.post(URL , data=PARAMS_3, files=dict(foo='bar'))
        return

    def set_lengths(self, data):
        '''Get length of the User sets'''
        length=[]
        sts=['Section_3/Set_0','Section_4/Set_2','Section_4/Set_3','Section_4/Set_6','Section_4/Set_7']
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
        
    def Entry_Generator_Paper_Supplements(self, props, relations, add_relations):
        '''This function takes a paper supplement (i.e. authors, languages, journal) and creates the corresponding wikibase entries.'''
        qids = []
        for prop in props:
            if prop:
                prop = prop.split(' <|> ')
                if re.match(r"mardi:Q[0-9]+", prop[0]):
                    # If supplement  on MaRDI Portal store QID
                    qids.append(prop[0].split(':')[1])
                elif re.match(r"wikidata:Q[0-9]+", prop[0]):
                    # If supplement on Wikidata check if similar entity exist in MarDI KG and use or create dummy Wikidata entry
                    req = {}
                    try:
                        req = requests.get(mardi_api+'?action=wbsearchentities&format=json&language=en&type=item&limit=10&search={0}'.format(prop[1]),
                                           headers = {'User-Agent': 'MaRDMO_0.1 (https://zib.de; reidelbach@zib.de)'}
                                          ).json()['search'][0]
                    except (KeyError,IndexError):
                        # KeyError: search string is empty
                        # IndexError: no result found for string
                        pass
                    if req:
                        #If supplement with Wikidata Label Description on MaRDI Portal, store QID
                        if req['display']['label']['value'] == prop[1] and req['display']['description']['value'] == prop[2]:
                            qids.append(req['id'])
                        else:
                            qids.append(self.entry(prop[1], prop[2], [(ExternalID, prop[0].split(':')[1], P2)]))
                    else:
                        qids.append(self.entry(prop[1], prop[2], [(ExternalID, prop[0].split(':')[1], P2)]))
                else:
                    # If supplement not on MaRDI KG or Wikidata check if Entity with standard label and description exists and use it or create it
                    req = {}
                    try:
                        req = requests.get(mardi_api+'?action=wbsearchentities&format=json&language=en&type=item&limit=10&search={0}'.format(prop[1]),
                                           headers = {'User-Agent': 'MaRDMO_0.1 (https://zib.de; reidelbach@zib.de)'}
                                          ).json()['search'][0]
                    except (KeyError,IndexError):
                        # KeyError: search string is empty
                        # IndexError: no result found for string
                        pass
                    if add_relations:
                        # For Authors additional relations are required
                        relations += [(ExternalID, p.split(':')[1], P22 if p.split(':')[0] == 'orcid' else P23 if p.split(':')[0] == 'zbmath' else '') for p in prop[0].split('; ')] 
                    if req:
                        #If supplement with Wikidata Label Description on MaRDI Portal, store QID
                        if req['display']['label']['value'] == prop[1] and req['display']['description']['value'] == prop[2]:
                            qids.append(req['id'])
                        else:
                            qids.append(self.entry(prop[1], prop[2], relations))
                    else:
                        qids.append(self.entry(prop[1], prop[2], relations))
        return qids

    def sparql(self,data,ws,orcid=None,doi=None,cit=None):
        '''This function takes user answers and performs SPARQL queries to Wikidata and MaRDI portal.'''
        
        length = self.set_lengths(data)

        types = ['model', 'method', 'software', 'inputs', 'outputs', 'disciplines','fields']
        strings = ['mod', 'met', 'sof', 'inp', 'out', 'dis','fie']
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
            
            x.append(self.wikibase_answers(data, ws[ABBR], length[IDX]) if ABBR not in ('dis','fie') else self.wikibase_answers(data, ws[ABBR])[0].split('; '))
            
            x.append(length[IDX] if ABBR not in ('dis','fie') else len(x[0]) if x else 0)

            x.append([re.split(' <\|> ', x[0][i]) if x[0][i] and x[0][i] != 'not in MathModDB' else 
                     ['', x[0][x[1] + i] if ABBR in strings[:5] else '',
                      x[0][x[1] * 2 + i] if ABBR in strings[:3] else 'data set' if ABBR in strings[3:5] else ''] for i in range(x[1])])

            # For existing software get programming languages from KGs (might be extended for further information)
            if ABBR in ('sof'):
                for i in range(x[1]):
                    res = self.get_pl(x[2][i][0])
                    if res:
                        x[0][3*x[1]+i] = res
            
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
                                                                       wq['wq'+s+str(i)]["quote"].replace("'",r"\'")),'1')
                                                                       for i in range(user_answers[d][1])})

            if s in strings[:3]:

                wq.update({'wq'+s+'_sub'+str(i)+'_'+str(j): {'qid': f[0].split(':'), 'label':f[1], 'quote':f[2]} for i,ss in enumerate(user_answers[d][4]) for j,f in enumerate(ss[3])})

                qm.update({'mq'+s+'_sub'+str(i)+'_'+str(j) : mini.format('?qid',mbody.format(wq['wq'+s+'_sub'+str(i)+'_'+str(j)]['label'].replace("'",r"\'"),
                                                                                             wq['wq'+s+'_sub'+str(i)+'_'+str(j)]['quote'].replace("'",r"\'")),'1')
                                                                                             for i,ss in enumerate(user_answers[d][4]) for j,_ in enumerate(ss[3])})
        
        ### Request Data from MaRDI KG

        for key in qm.keys():
            mq.update({key:{**dict.fromkeys({'qid'},{'value':''}),**self.get_results(mardi_endpoint,qm[key])[0]}})
        
        return wq, mq

    def Entry_Generator(self,Type,Sub_Type,Generate,Relations,wq,mq,data):
        '''Function queries Wikidata/MaRDI KG, uses and generates entries in MaRDI Knowledge Graph.'''
    
        try:
            del data[ws[Type][0]]
        except:
            pass
    
        qids=[]
        for i in range(wq['no'][Type]):
            
            # Hyperlinks for Software (extendable to others)
            if Type == 'sof':
                for vdp in VDP:
                    if vdp+'_'+str(i) in data.keys():
                        data.update({vdp+'_'+str(i):re.sub(r'Yes: (\S+)',r'[Yes](\1)',data[vdp+'_'+str(i)])})

            # Check if on Portal or in Wikidata, integrate Wikidata entry if desired
            qid,entry=self.portal_wikidata_check(mq['mq'+Type+str(i)],wq['wq'+Type+str(i)],data)

            # Update User answers
            if entry and qid:
                qids.append(qid)
                if Type in ('dis','fie'):
                    data.update({ws[Type][0]+'_'+str(i):'{0} - [{1}]({2}Item:{3})'.format(str(i+1),entry[0],mardi_wiki,qid)})
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
                            sub_qid_str+='[{0}]({1}Item:{2});'.format(entry[0],mardi_wiki,sub_qid)
                     
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

    def get_pl(self,soft_id):
        '''Frunction gets programming language information from KGs if User selects existing software'''
        R=''
        if soft_id.split(':')[0] == 'wikidata':
            res = self.get_results(wikidata_endpoint,wini.format(pl_vars,pl_query.format(soft_id.split(':')[-1],'P277'),'100'))
            R=('; ').join(['wikidata:'+r['qid']['value']+' <|> '+r['label']['value']+' <|> '+r['quote']['value'] if ('qid' and 'label' and 'quote') in r.keys() else '' for r in res])
        elif soft_id.split(':')[0] == 'mardi':
            res = self.get_results(mardi_endpoint,mini.format(pl_vars,pl_query.format(soft_id.split(':')[-1],P19),'100'))
            R=('; ').join(['mardi:'+r['qid']['value']+' <|> '+r['label']['value']+' <|> '+r['quote']['value'] if ('qid' and 'label' and 'quote') in r.keys() else '' for r in res])
        return R

            
    def get_answer(self, uri):
        '''Function that retrieves individual User answers'''
        val =[]
        values = self.project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri=uri))
        for value in values:
            if value.option_text:
                val.append(value.option_text)
            if value.text:
                val.append(value.text)
        return val

