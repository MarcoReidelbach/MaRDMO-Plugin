import re
import requests
import os
import time
from django.http import HttpResponse
from django.shortcuts import redirect, render, reverse
from django.utils.translation import gettext_lazy as _
from django.template import Template, Context

from rdmo.projects.exports import Export
from rdmo.views.utils import ProjectWrapper
from rdmo.views.templatetags import view_tags
from rdmo.domain.models import Attribute

from wikibaseintegrator import wbi_login, WikibaseIntegrator
from wikibaseintegrator.datatypes import ExternalID, Item, String, Time, MonolingualText, Quantity
from wikibaseintegrator.wbi_enums import ActionIfExists
from wikibaseintegrator.wbi_config import config as wbi_config
from wikibaseintegrator.models import Qualifiers

from .para import *
from .config import *
from .citation import *
from .id import *
from .sparql import *
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
            return render(self.request,'MaRDMO/workflowError.html', {
                'error': 'Questionnaire \'{}\' not suitable for MaRDI Export!'.format(str(self.project.catalog).split('/')[-1])
                }, status=200)
        
### Gather all User Answers in Dictionary ########################################################################################################################################################
        
        answers ={}
        for label, info in questions.items():
            answers = self.get_answer(answers,**info)
        
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
        if answers['Settings'].get('Documentation') == option['Documentation']:

### Checks for Workflow Documentation #############################################################################################################################################################

            # Login Credentials for MaRDI Portal Export
            if answers['Settings']['Public'] == option['Public'] and answers['Settings']['Preview'] == option['No']:
                if not (lgname and lgpassword):
                    #Stop if no Login Credentials are provided
                    return render(self.request,'MaRDMO/workflowError.html', {
                        'error': 'No permission to write to MaRDI Portal. Check Bot Credentials.'
                        }, status=200)

            # Documentation Type
            if answers['Settings'].get('DocumentationType')  == option['Workflow']:
            
                # Workflow Type (THEO/EXP)
                if answers['Settings'].get('WorkflowType')  not in (option['Computation'], option['Analysis']): 
                    # Stop if no Workflow Type is chosen
                    return render(self.request,'MaRDMO/workflowError.html', {
                        'error': 'Missing Workflow Type!'
                        }, status=200)

                # Research Objective Provided
                if not answers['GeneralInformation'].get('ResearchObjective'):
                    # Stop if no Research Objective is provided
                    return render(self.request,'MaRDMO/workflowError.html', {
                        'error': 'Missing Research Objective!'
                        }, status=200)

                # Identical Workflow on MaRDI Portal
                if answers['Settings']['Public'] == option['Public'] and answers['Settings']['Preview'] == option['No']: 
                    # Evaluate user-defined Workflow Author Name and ID(s)
                    if not answers['Creator'].get('Name'):
                        # Stop if no Workflow Author Name provided
                        return render(self.request,'MaRDMO/workflowError.html', {
                            'error': 'Missing Name of Workflow Documentation Creator'
                            }, status=200)
                    if answers['Creator'].get('IDs'):
                        # If ID(s) provided, check if they match the author ID(s) on MaRDI Portal. If yes, allow edits.
                        creator_orcid_id = []; creator_zbmath_id = []
                        orcid_creator = []; zbmath_creator = []
                        for user_id in answers['Creator']['IDs'].values():
                            user_id = user_id.split(':')
                            if user_id[0] == 'orcid':
                                creator_orcid_id.append(user_id[1])
                                orcid_creator.extend([[answers['Creator']['Name'],user_id[1]]])
                            elif user_id[0] == 'zbmath':
                                creator_zbmath_id.append(user_id[1])
                                zbmath_creator.extend([[answers['Creator']['Name'], user_id[1]]])
                            else:
                                # Stop if wrong ID type provided for Workflow author
                                return render(self.request,'MaRDMO/workflowError.html', {
                                    'error': 'Identifier of Workflow Documentation Creator not supported'
                                    }, status=200)
                    else:
                        # Stop if no ID(s) provided
                        return render(self.request,'MaRDMO/workflowError.html', {
                            'error': 'Missing Identifier of Workflow Documentation Creator'
                            }, status=200)
                
                    # Check if Workflow with same Label and Description on MaRDI Portal, get workflow author credentials
                    req = self.get_results(mardi_endpoint,
                                           mini.format('?qid ?orcid ?zbmath',mbody2.format(self.project.title.replace("'",r"\'"),
                                                                                           answers['GeneralInformation']['ResearchObjective'].replace("'",r"\'"),
                                                                                           P8,P22,P23),'1'))[0]
                    existing_workflow_qid = None
                    if req.get('qid', {}).get('value'):
                        # Store Workflow QID and Workflow Author  credentials
                        existing_workflow_qid = req['qid']['value']
                        workflow_author_orcid = req.get('orcid', {}).get('value')
                        workflow_author_zbmath = req.get('zbmath', {}).get('value')
                        if answers['Creator']['IDs']:
                            # If ID(s) provided, check if they match the author ID(s) on MaRDI Portal. If yes, allow edits.
                            edit_allowed = True
                            for user_id in answers['Creator']['IDs'].values():
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
                            return render(self.request,'MaRDMO/workflowError.html', {
                                'error': 'Workflow already exists on MaRDI Portal'
                                }, status=200)
                else:
                    creator_orcid_id = ''; orcid_creator = ''
                    creator_zbmath_id = ''; zbmath_creator = ''
 
### If Portal Integration desired, check if Paper already exists on MaRDI Portal or Wikidata  #####################################################################################################

                # If Portal integration wanted, get further publication information
                if answers['Settings']['Public'] == option['Public'] and answers['Settings']['Preview'] == option['No']:
                    if answers['Publication']['Exists'][0] == option['YesText']:
                        # Extract Paper DOI
                        doi=re.split(':', answers['Publication']['Exists'][1],1)

                        if doi[0] == 'doi':
                            
                            if not doi[-1]:
                                # Stop if no DOI provided
                                return render(self.request,'MaRDMO/workflowError.html', {
                                    'error': 'Missing DOI of related Publication!'
                                    }, status=200)

                            if not answers['Publication']['Info']:
                                # Stop if no Information available via DOI
                                return render(self.request,'MaRDMO/workflowError.html', {
                                    'error': 'DOI for related Publication returns no Information!'
                                    }, status=200)

                            # Get Publication ID, Label and Description
                            answers['Publication']['Info'] = answers['Publication']['Info'].split(' <|> ')
                
                            if re.match(r"mardi:Q[0-9]+", answers['Publication']['Info'][0]):
                                # If Paper with DOI on MaRDI Portal store QID
                                paper_qid= answers['Publication']['Info'][0].split(':')[1]

                            elif re.match(r"wikidata:Q[0-9]+", answers['Publication']['Info'][0]): 
                                # If Paper with DOI on Wikidata, generate dummy entry  store QID
                                paper_qid= self.entry(answers['Publication']['Info'][1], answers['Publication']['Info'][2], [(ExternalID, answers['Publication']['Info'][0].split(':')[1], P2)])

                            else:
                        
### Create New Publication Entry ##################################################################################################################################################################
### Prepare User edited Authors  ##################################################################################################################################################################
                        
                                orcid_ids = []
                                orcid_authors = []
                                zbmath_ids = []
                                zbmath_authors = []
                                authors_remove = []
                        
                                # Identify Authors with ID added by User
                                other_authors = list(answers['Publication'].get('All Authors',{}).values())[len(list(answers['Publication'].get('Identified Authors',{}).values())):]
                    
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
                                answers['Publication'].setdefault('Identified Authors',{})
                                for idx, (author_id, author_data) in enumerate(author_dict_merged.items()):
                                    if author_data['mardiQID']:
                                        answers['Publication']['Identified Authors'].update({f"n{idx}":f"mardi:{author_data['mardiQID']}"})
                                    elif author_data['wikiQID']:
                                        answers['Publication']['Identified Authors'].update({f"n{idx}":f"wikidata:{author_data['wikiQID']} <|> {author_data['wikiLabel']} <|> {author_data['wikiDescription']}"})
                                    else:
                                        if author_data['orcid']:
                                            orcid_info = f"orcid:{author_data['orcid']}"
                                            if author_data['zbmath']:
                                                orcid_info += f"; zbmath:{author_data['zbmath']}"
                                            answers['Publication']['Identified Authors'].update({f"n{idx}":f"{orcid_info} <|> {author_id} <|> researcher (ORCID {author_data['orcid']})"})
                                        elif author_data['zbmath']:
                                            answers['Publication']['Identified Authors'].update({f"n{idx}":f"zbmath:{author_data['zbmath']} <|> {author_id} <|> researcher (zbMath {author_data['zbmath']})"})

### Add Authors, Language and Journal of Paper to MaRDI Portal #####################################################################################################################################
                        
                                author_qids = self.Entry_Generator_Paper_Supplements(answers['Publication']['Identified Authors'],
                                                                                     [(Item, Q7, P4), (Item, Q8, P21)],
                                                                                     True)
                         
                                language_qids = self.Entry_Generator_Paper_Supplements({'Language':answers['Publication'].get('Language')},
                                                                                       [(Item, Q11, P4)],
                                                                                       False)

                                journal_qids = self.Entry_Generator_Paper_Supplements({'Journal':answers['Publication'].get('Journal')},
                                                                                      [(Item, Q9, P4)],
                                                                                      False)

### Add Paper to  MaRDI Portal ####################################################################################################################################################################
                        
                                paper_qid=self.entry(answers['Publication']['Info'][1], answers['Publication']['Info'][2], 
                                                     [(Item, answers['Publication']['Type'].split(' <|> ')[0].split(':')[1], P4)] +
                                                     [(Item, author, P8) for author in author_qids] +
                                                     [(String, author, P9) for author in other_authors] +
                                                     [(Item, language, P10) for language in language_qids] +
                                                     [(Item, journal, P12) for journal in journal_qids] +
                                                     [(MonolingualText, answers['Publication'].get('Title'), P7),
                                                      (Time, answers['Publication'].get('Date')[:10]+'T00:00:00Z', P11),
                                                      (String, answers['Publication'].get('Volume'), P13),
                                                      (String, answers['Publication'].get('Issue'), P14),
                                                      (String, answers['Publication'].get('Pages'), P15),
                                                      (ExternalID,doi[-1].upper(),P16)])
                        
                        elif doi[0] == 'url':
                            paper_qid = doi[1]

                    else:
                        # No DOI provided
                        paper_qid=''

### Get Information of Workflow Creator and add Information to MaRDI Portal  ######################################################################################################################
            
                creator_dict_merged = Author_Search(creator_orcid_id, creator_zbmath_id, orcid_creator, zbmath_creator)
                       
                creators = {}
                for idx, (author_id, author_data) in enumerate(creator_dict_merged.items()):
                    if author_data['mardiQID']:
                        creators.update({f"{idx}":f"mardi:{author_data['mardiQID']}"})
                    elif author_data['wikiQID']:
                        creators.update({f"{idx}":f"wikidata:{author_data['wikiQID']} <|> {author_data['wikiLabel']} <|> {author_data['wikiDescription']}"})
                    else:
                        if author_data['orcid']:
                            orcid_info = f"orcid:{author_data['orcid']}"
                            if author_data['zbmath']:
                                orcid_info += f"; zbmath:{author_data['zbmath']}"
                            creators.update({f"{idx}":f"{orcid_info} <|> {author_id} <|> researcher (ORCID {author_data['orcid']})"})
                        elif author_data['zbmath']:
                            creators.update({f"{idx}":f"zbmath:{author_data['zbmath']} <|> {author_id} <|> researcher (zbMath {author_data['zbmath']})"})

                creator_qids = self.Entry_Generator_Paper_Supplements(creators,
                                                                     [(Item, Q7, P4), (Item, Q8, P21)],
                                                                     True)

### Refine User Answers via External Data Sources #################################################################################################################################################
            
                answers = self.refine(answers)
                 
### Integrate related Model in MaRDI KG ###########################################################################################################################################################
                 
                models, answers, error = self.Entry_Generator('Models',              # Entry of Model
                                                              [True,False,False],   # Generation wanted, QID Generation wanted, String Generation not wanted
                                                              [Q3,P17],             # instance of mathematical model (Q3), main subject (P17)
                                                              answers)              # refined user answers
             
                if error[0] == 0:
                    # Stop if no Name and Description provided for new model entry
                    return render(self.request,'MaRDMO/workflowError.html', {
                        'error': 'Missing Name and/or Description of new Mathematical Model!'
                        }, status=200)

                elif error[0] == 1:
                    #Stop if no main subject provided for new model entry
                    return render(self.request,'MaRDMO/workflowError.html', {
                        'error': 'Missing Main Subject of new Mathematical Model!'
                        }, status=200)
                
                # Add Symbols to Task Quantities
                for tkey in answers['Task']:
                    for tkey2 in answers['Task'][tkey]['Other2']:
                        tvar = answers['Task'][tkey]['Other2'][tkey2].split(' <|> ')[1]
                        for mkey in answers['MathematicalFormulation']:
                            for mkey2 in answers['MathematicalFormulation'][mkey]['Element']:
                                mvar = answers['MathematicalFormulation'][mkey]['Element'][mkey2]['Quantity'].split(' <|> ')[1]
                                if tvar == mvar:
                                    answers['Task'][tkey].setdefault('RelationQ',{}).update({tkey2:[answers['Task'][tkey]['Relation2'][tkey2],tvar.rsplit(' ',1)[0],answers['MathematicalFormulation'][mkey]['Element'][mkey2]['Symbol']]})
                            
### Integrate related Methods in MaRDI KG #########################################################################################################################################################

                methods, answers, error = self.Entry_Generator('Method',            # Entry of Method with Main Subject
                                                               [True,True,False],   # Generation wanted, QID Generation wanted, String Generation not wanted
                                                               [Q4,P17],            # instance of method (Q4), main subject (P17)
                                                               answers)             # refined user answers

                if error[0] == 0:
                    # Stop if no Name and Description provided for new method entry
                    return render(self.request,'MaRDMO/workflowError.html', {
                        'error': 'Missing Name and/or Description of new Mathematical Method in Set {}!'.format(error[1])
                        }, status=200)
            
                elif error[0] == 1:
                    #Stop if no main subject provided for new method entry
                    return render(self.request,'MaRDMO/workflowError.html', {
                        'error': 'Missing Main Subject of new Mathematical Method in Set {}!'.format(error[1])
                        }, status=200)

                for mkey in answers['Method']:
                    i=0
                    for pkey in answers['ProcessStep']:
                        if answers['ProcessStep'][pkey].get('Method'):
                            for pkey2 in answers['ProcessStep'][pkey]['Method']:
                                if answers['Method'][mkey]['Name'] == answers['ProcessStep'][pkey]['Method'][pkey2]:
                                    answers['Method'][mkey].setdefault('ProcessStep',{}).update({i:answers['ProcessStep'][pkey]['Name']})
                                    i=i+1
            
### Integrate related Softwares in MaRDI KG #######################################################################################################################################################
            
                softwares, answers, error = self.Entry_Generator('Software',        # Entry of Software with Programming Languages 
                                                                 [True,True,True],  # Generation wanted, QID Generation wanted, String Generation wanted
                                                                 [Q5,P19],          # instance of software (Q5), programmed in (P19)
                                                                 answers)           # refined user answers

                if error[0] == 0:
                    # Stop if no Name and Description provided for new software entry
                    return render(self.request,'MaRDMO/workflowError.html', {
                        'error': 'Missing Name and/or Description of new Software in Set {}!'.format(error[1])
                        }, status=200)
            
                elif error[0] == 1:
                    #Stop if no programming language provided for new software entry
                    return render(self.request,'MaRDMO/workflowError.html', {
                        'error': 'Missing Programming Language(s) of new Software in Set {}!'.format(error[1])
                        }, status=200)
             
                for skey in answers['Software']:
                    for dkey in answers['ExperimentalDevice']:
                        if answers['ExperimentalDevice'][dkey].get('SubProperty2'):
                            for dkey2 in answers['ExperimentalDevice'][dkey]['SubProperty2']:
                                if answers['Software'][skey]['Name'] == answers['ExperimentalDevice'][dkey]['SubProperty2'][dkey2]['Name'] and answers['Software'][skey]['Description'] == answers['ExperimentalDevice'][dkey]['SubProperty2'][dkey2]['Description']:
                                    answers['ExperimentalDevice'][dkey]['SubProperty2'][dkey2]['ID'] = 'mardi:'+answers['Software'][skey]['mardiId']

### Hardware/Devices #############################################################################################################################################################################

                if answers['Settings']['WorkflowType'] == option['Computation']: 
                
                    # Hardware
                    hardwares, answers, error = self.Entry_Generator('Hardware',                     # Entry of Hardware
                                                                     [True,True,False],              # Generation wanted, QID Generation wanted, String Generation not wanted
                                                                     [Q12,P26,P6,P4,P32,P2,P27,P31], # nothing
                                                                     answers)                        # refined user answers  

                    if error[0] == 0:
                        # Stop if no Name and Description provided for new method entry
                        return render(self.request,'MaRDMO/workflowError.html', {
                            'error': 'Missing Name and/or Description of new Hardware in Set {}!'.format(error[1])
                            }, status=200)
            
                elif answers['Settings']['WorkflowType'] == option['Analysis']:
            
                    # Devices
                    devices, answers, error = self.Entry_Generator('ExperimentalDevice',           # Entry of Hardware
                                                                   [True,True,False],              # Generation wanted, QID Generation wanted, String Generation not wanted
                                                                   [Q13,P28,P6,P29,P30],           # nothing
                                                                   answers)                        # refined user answers  

                    if error[0] == 0:
                        # Stop if no Name and Description provided for new method entry
                        return render(self.request,'MaRDMO/workflowError.html', {
                            'error': 'Missing Name and/or Description of new Hardware in Set {}!'.format(error[1])
                            }, status=200)

### Integrate related Data Sets in MaRDI KG #######################################################################################################################################################
            
                datas, answers, error = self.Entry_Generator('DataSet',            # Entry of Data Set
                                                              [True,False,False],   # Generation wanted, QID Generation not wanted, String Generation not wanted
                                                              [Q6,''],              # instance of data set (Q6)
                                                              answers)              # refined user answers

                if error[0] == 0:
                    # Stop if no Name and Description provided for new input data set
                    return render(self.request,'MaRDMO/workflowError.html', {
                        'error': 'Missing Name of new Input Data in Set {}!'.format(error[1])
                        }, status=200)
       
                for dkey in answers['DataSet']:
                    for pkey in answers['ProcessStep']:
                        if answers['ProcessStep'][pkey].get('Input'):
                            for pkey2 in answers['ProcessStep'][pkey]['Input']:
                                if answers['DataSet'][dkey]['Name'] == answers['ProcessStep'][pkey]['Input'][pkey2]:
                                    answers['DataSet'][dkey].setdefault('Type',{}).update({0:'Input'})
                        if answers['ProcessStep'][pkey].get('Output'):
                            for pkey2 in answers['ProcessStep'][pkey]['Output']:
                                if answers['DataSet'][dkey]['Name'] == answers['ProcessStep'][pkey]['Output'][pkey2]:
                                    answers['DataSet'][dkey].setdefault('Type',{}).update({1:'Output'})
        
### Integrate related non-mathematical Disciplines in MaRDI KG ####################################################################################################################################
            
                if answers['NonMathematicalDiscipline'].get(0,{}).get('ID'):
                    answers.update({'NonMathematicalDiscipline':answers['NonMathematicalDiscipline'][0]['ID']})
                else:
                    return render(self.request,'MaRDMO/workflowError.html', {
                        'error': 'Missing Non-Mathematical Disciplines of Workflow!'
                        }, status=200)

                disciplines, answers, error = self.Entry_Generator('NonMathematicalDiscipline',     # Entry of non-mathmatical Disciplines
                                                                   [False,False,False],             # Generation not wanted, QID Generation not wanted, String Generation not wanted
                                                                   ['',''],                         # nothing
                                                                   answers)                         # refined user answers

### Mathematical Fields ###########################################################################################################################################################################
            
                if answers['MathematicalArea'].get(0,{}).get('ID'):
                    answers.update({'MathematicalArea':answers['MathematicalArea'][0]['ID']})
                else:
                    # Stop if no Mathematical Field provided by User
                    return render(self.request,'MaRDMO/workflowError.html', {
                        'error': 'Missing Mathematical Fields of Workflow!'
                        }, status=200)
            
### Integrate Workflow in MaRDI KG ################################################################################################################################################################

                if answers['Settings']['Public'] == option['Public'] and answers['Settings']['Preview'] == option['No']: 
                    # Facts for MaRDI KG Integration
                    facts = [(Item,Q2,P4),(Item,paper_qid,P3) if re.match(r"Q[0-9]+",paper_qid) else (ExternalID,paper_qid,P24)] +\
                            [(Item,discipline,P5) for discipline in disciplines] +\
                            [(ExternalID,field,P25) for field in answers['MathematicalArea'].values()] +\
                            [(Item, creator, P8) for creator in creator_qids] +\
                            [(Item,i,P6) for i in methods+models]        

                    if answers['Settings']['WorkflowType'] == option['Computation']:

                        # Add Hardware Facts for Computational Workflow
                        facts += [(Item,i,P6,answers['Hardware'][idx]['Qualifiers']) for idx,i in enumerate(hardwares)] 

                    elif answers['Settings']['WorkflowType'] == option['Analysis']:

                        # Add Device Facts for Data Analysis Workflow
                        facts += [(Item,i,P6,answers['ExperimentalDevice'][idx]['Qualifiers']) for idx,i in enumerate(devices)]

                    # If MaRDI KG integration is desired
                    if existing_workflow_qid:
                        wbi = self.wikibase_login()
                        item = wbi.item.get(existing_workflow_qid)
                        for claim in item.claims.claims:
                            item.claims.remove(claim)
                        item.write()
                        wbi = self.wikibase_login()
                        item = wbi.item.get(existing_workflow_qid)       
                        d=[]
                        for fact in facts:
                            if fact[1]:
                                if fact[0] == MonolingualText:
                                    d.append(fact[0](text=fact[1],prop_nr=fact[2]))
                                elif fact[0] == Time:
                                    d.append(fact[0](time=fact[1],prop_nr=fact[2]))
                                else:
                                    if len(fact) == 3:
                                        d.append(fact[0](value=fact[1],prop_nr=fact[2]))
                                    elif len(fact) == 4:
                                        d.append(fact[0](value=fact[1],prop_nr=fact[2],qualifiers=fact[3]))
                        item.claims.add(d)
                        item.write()
                        workflow_qid = item.id
                    else:
                        workflow_qid=self.entry(self.project.title, answers['GeneralInformation']['ResearchObjective'], facts)

### Generate and Publish Workflow Page ############################################################################################################################################################
            
                # Download Workflow Doucmentation as Markdown File
                if answers['Settings']['Public'] == option['Local']:
                
                    # Load MaRDI Markdown Workflow Template
                    path = os.path.join(os.path.dirname(__file__), 'templates', 'MaRDMO', 'workflowTemplate.md')
                    with open(path, 'r') as file:
                        markdown_template = file.read()

                    # Create a Django Template object
                    template = Template(markdown_template)
                    
                    # Render the template with the data
                    context = Context({'title':self.project.title}|answers|option)
                    markdown_workflow = template.render(context)
                
                    # Provide Documentation as Markdown Download
                    response = HttpResponse(os.linesep.join([s.strip() for s in markdown_workflow.splitlines() if s.strip()]), content_type="application/md")
                    response['Content-Disposition'] = 'filename="workflow.md"'
                
                    return response
            
                # Preview Workflow Documentation as HTML File
                elif answers['Settings']['Public'] == option['Public'] and answers['Settings']['Preview'] == option['Yes']:

                    return render(self.request,'MaRDMO/workflowTemplate.html', {
                        'title': self.project.title,
                        'answers': answers,
                        'option': option
                        }, status=200)
            
                # Export Workflow Documentation to MaRDI Portal as Mediawiki File
                elif answers['Settings']['Public'] == option['Public'] and answers['Settings']['Preview'] == option['No']:

                    # Load MaRDI Markdown Workflow Template
                    path = os.path.join(os.path.dirname(__file__), 'templates', 'MaRDMO', 'workflowTemplate.mediawiki')
                    with open(path, 'r') as file:
                        mediawiki_template = file.read()

                    # Create a Django Template object
                    template = Template(mediawiki_template)

                    # Render the template with the data
                    context = Context(answers|option)
                    mediawiki_workflow = template.render(context)

                    # Export to MaRDI Portal
                    self.wikipage_export(self.project.title,os.linesep.join([re.sub(r'\$\$\s?(.*?)\$\$',r'<math>\1</math>',s.strip()) for s in mediawiki_workflow.splitlines() if s.strip()]))

                    # Successful Export to Portal
                    return render(self.request,'MaRDMO/workflowExport.html', {
                        'WikiLink': mardi_wiki+self.project.title.replace(' ','_'),
                        'KGLink': mardi_wiki+'Item:'+workflow_qid
                        }, status=200)
            
                else:
                    # Stop if no Export Type is chosen
                    return render(self.request,'MaRDMO/workflowError.html', {
                        'error': 'Missing Export Type!'
                        }, status=200)

            elif answers['Settings'].get('DocumentationType')  == option['Documentation'] or answers['Settings'].get('DocumentationType')  == option['Model']:
            
                # Mathematical Model documentation soon be integrated
                answers = self.refine(answers)
               
                # Evaluate user-defined Model Author Name
                if answers['Creator'].get('Name'):
                    Surname, GivenName = answers['Creator']['Name'].split(',')
                    answers['Creator'].update({'Surname':Surname,'GivenName':GivenName})
                else:
                    # Stop if no Workflow Author Name provided
                    return render(self.request,'MaRDMO/workflowError.html', {
                        'error': 'Missing Name of Model Documentation Creator'
                        }, status=200)
                
                # Evaluate user-defined Model Author ID(s)
                if answers['Creator'].get('IDs'):
                    # Check if IDs provided
                    orcidID = []; zbmathID = []
                    for user_id in answers['Creator']['IDs'].values():
                        user_id = user_id.split(':')
                        if user_id[0] == 'orcid':
                            answers['Creator'].setdefault('orcidID',[]).append(user_id[1])
                        elif user_id[0] == 'zbmath':
                            answers['Creator'].setdefault('zbmathID',[]).append(user_id[1])
                        else:
                            # Stop if wrong ID type provided for Workflow author
                            return render(self.request,'MaRDMO/workflowError.html', {
                                'error': 'Identifier of Model Documentation Creator not supported'
                                }, status=200)
                else:
                    # Stop if no ID(s) provided
                    return render(self.request,'MaRDMO/workflowError.html', {
                        'error': 'Missing Identifier of Model Documentation Creator'
                        }, status=200)

                ### GET ADDITIONAL INFORMATION FROM MATHMODDB
                
                # Get additional Model Information (additional Models)

                keys = list(answers['AdditionalModel'])

                for key in keys:
                    if answers['AdditionalModel'][key]['MathModID'] and answers['AdditionalModel'][key]['MathModID'] != 'not in MathModDB':
                
                        req=requests.get('https://sparql.ta4.m1.mardi.ovh/mathalgodb/query',
                                         params = {'format': 'json', 'query': query_mm.format(answers['AdditionalModel'][key]['MathModID'].split('#')[1])},
                                         headers = {'User-Agent': 'MaRDMO_0.1 (https://zib.de; reidelbach@zib.de)'}).json()['results']['bindings']
                        
                        req2=requests.get('https://sparql.ta4.m1.mardi.ovh/mathalgodb/query',
                                          params = {'format': 'json', 'query': query_mm2.format(answers['AdditionalModel'][key]['MathModID'].split('#')[1])},
                                          headers = {'User-Agent': 'MaRDMO_0.1 (https://zib.de; reidelbach@zib.de)'}).json()['results']['bindings']
                    
                        for r in req:
                            if r.get('quote', {}).get('value'):
                                answers['AdditionalModel'][key].update({'Description':r['quote']['value']})
                           
                            if r.get('convex',{}):
                                if r['convex']['value'] == 'true':
                                    answers['AdditionalModel'][key].setdefault('Properties',{}).update({0:option['IsConvex']})
                                else:
                                    answers['AdditionalModel'][key].setdefault('Properties',{}).update({1:option['IsNotConvex']})
                            
                            if r.get('deterministic',{}):
                                if r['deterministic']['value'] == 'true':
                                    answers['AdditionalModel'][key].setdefault('Properties',{}).update({2:option['IsDeterministic']})
                                else:
                                    answers['AdditionalModel'][key].setdefault('Properties',{}).update({3:option['IsStochastic']})
                            
                            if r.get('dimensionless',{}):
                                if r['dimensionless']['value'] == 'true':
                                    answers['AdditionalModel'][key].setdefault('Properties',{}).update({4:option['IsDimensionless']})
                                else:
                                    answers['AdditionalModel'][key].setdefault('Properties',{}).update({5:option['IsDimensional']})
                            
                            if r.get('dynamic',{}):
                                if r['dynamic']['value'] == 'true':
                                    answers['AdditionalModel'][key].setdefault('Properties',{}).update({6:option['IsDynamic']})
                                else:
                                    answers['AdditionalModel'][key].setdefault('Properties',{}).update({7:option['IsStatic']})
                            
                            if r.get('linear',{}):
                                if r['linear']['value'] == 'true':
                                    answers['AdditionalModel'][key].setdefault('Properties',{}).update({8:option['IsLinear']})
                                else:
                                    answers['AdditionalModel'][key].setdefault('Properties',{}).update({9:option['IsNotLinear']})
                            
                            if r.get('spacecont',{}):
                                if r['spacecont']['value'] == 'true':
                                    answers['AdditionalModel'][key].setdefault('Properties',{}).update({10:option['IsSpaceContinuous']})
                                else:
                                    answers['AdditionalModel'][key].setdefault('Properties',{}).update({11:option['IsSpaceDiscrete']})
                            else:
                                answers['AdditionalModel'][key].setdefault('Properties',{}).update({12:option['IsSpaceIndependent']})
                            
                            if r.get('timecont',{}):
                                if r['timecont']['value'] == 'true':
                                    answers['AdditionalModel'][key].setdefault('Properties',{}).update({13:option['IsTimeContinuous']})
                                else:
                                    answers['AdditionalModel'][key].setdefault('Properties',{}).update({14:option['IsTimeDiscrete']})
                            else:
                                answers['AdditionalModel'][key].setdefault('Properties',{}).update({15:option['IsTimeIndependent']})
                            
                            if r.get('P', {}).get('value') and r.get('PL', {}).get('value'):
                                for idx, (Id, label) in enumerate(zip(r['P']['value'].split(' <|> '),r['PL']['value'].split(' <|> '))):
                                    if f"{Id} <|> {label}" not in answers['AdditionalModel'][key].setdefault('ResearchProblem',{}).values():
                                        answers['AdditionalModel'][key].setdefault('ResearchProblem',{}).update({f"pp{idx}":f"{Id} <|> {label}"})

                            if r.get('CMM', {}).get('value') and r.get('CMML', {}).get('value'):
                                for idx, (Id, label) in enumerate(zip(r['CMM']['value'].split(' <|> '),r['CMML']['value'].split(' <|> '))):
                                    answers['AdditionalModel'][key].setdefault('Relation1', {}).update({f'mm{idx}': option['ContainsModel']})
                                    answers['AdditionalModel'][key].setdefault('Other1', {}).update({f'mm{idx}': f'{Id} <|> {label}'})
                                    answers['AdditionalModel'].setdefault(max(answers['AdditionalModel'].keys())+1, {}).update({'MathModID': Id, 'Name': label})
                                    keys.append(max(answers['AdditionalModel'].keys()))

                            if r.get('F', {}).get('value') and r.get('FL', {}).get('value'):
                                for idx, (Id, label) in enumerate(zip(r['F']['value'].split(' <|> '),r['FL']['value'].split(' <|> '))):
                                    for k, math_form in answers['MathematicalFormulation'].items():
                                        if math_form.get('MathModID') == Id:
                                            math_form.setdefault('Relation1', {}).update({f'ff{idx}': option['ContainedAsFormulationIn']})
                                            math_form.setdefault('Other1', {}).update({f'ff{idx}': f"{answers['AdditionalModel'][key]['MathModID']} <|> {answers['AdditionalModel'][key]['Name']}"})
                                            break
                                    else:  # This else corresponds to the for loop, it runs if the loop is not broken
                                        if answers['MathematicalFormulation'].keys():
                                            new_key = max(answers['MathematicalFormulation'].keys())+1
                                        else:
                                            new_key = 0
                                        answers['MathematicalFormulation'].setdefault(new_key, {}).update({'MathModID': Id, 'Name': label})
                                        new_form = answers['MathematicalFormulation'][new_key]
                                        new_form.setdefault('Relation1', {}).update({f'ff{idx}': option['ContainedAsFormulationIn']})
                                        new_form.setdefault('Other1', {}).update({f'ff{idx}': f"{answers['AdditionalModel'][key]['MathModID']} <|> {answers['AdditionalModel'][key]['Name']}"})

                            if r.get('A', {}).get('value') and r.get('AL', {}).get('value'):
                                for idx, (Id, label) in enumerate(zip(r['A']['value'].split(' <|> '),r['AL']['value'].split(' <|> '))):
                                    for k, math_form in answers['MathematicalFormulation'].items():
                                        if math_form.get('MathModID') == Id:
                                            math_form.setdefault('Relation1', {}).update({f'aa{idx}': option['ContainedAsAssumptionIn']})
                                            math_form.setdefault('Other1', {}).update({f'aa{idx}': f"{answers['AdditionalModel'][key]['MathModID']} <|> {answers['AdditionalModel'][key]['Name']}"})
                                            break
                                    else:  # This else corresponds to the for loop, it runs if the loop is not broken
                                        if answers['MathematicalFormulation'].keys():
                                            new_key = max(answers['MathematicalFormulation'].keys())+1 
                                        else:
                                            new_key = 0
                                        answers['MathematicalFormulation'].setdefault(new_key, {}).update({'MathModID': Id, 'Name': label})
                                        new_form = answers['MathematicalFormulation'][new_key]
                                        new_form.setdefault('Relation1', {}).update({f'aa{idx}': option['ContainedAsAssumptionIn']})
                                        new_form.setdefault('Other1', {}).update({f'aa{idx}': f"{answers['AdditionalModel'][key]['MathModID']} <|> {answers['AdditionalModel'][key]['Name']}"})
                            
                            if r.get('BC', {}).get('value') and r.get('BCL', {}).get('value'):

                                for idx, (Id, label) in enumerate(zip(r['BC']['value'].split(' <|> '),r['BCL']['value'].split(' <|> '))):
                                    for k, math_form in answers['MathematicalFormulation'].items():
                                        if math_form.get('MathModID') == Id:
                                            math_form.setdefault('Relation1', {}).update({f'bc{idx}': option['ContainedBoundaryConditionIn']})
                                            math_form.setdefault('Other1', {}).update({f'bc{idx}': f"{answers['AdditionalModel'][key]['MathModID']} <|> {answers['AdditionalModel'][key]['Name']}"})
                                            break
                                    else:  # This else corresponds to the for loop, it runs if the loop is not broken
                                        if answers['MathematicalFormulation'].keys():
                                            new_key = max(answers['MathematicalFormulation'].keys())+1 
                                        else:
                                            new_key = 0
                                        answers['MathematicalFormulation'].setdefault(new_key, {}).update({'MathModID': Id, 'Name': label})
                                        new_form = answers['MathematicalFormulation'][new_key]
                                        new_form.setdefault('Relation1', {}).update({f'bc{idx}': option['ContainedAsBoundaryConditionIn']})
                                        new_form.setdefault('Other1', {}).update({f'bc{idx}': f"{answers['AdditionalModel'][key]['MathModID']} <|> {answers['AdditionalModel'][key]['Name']}"})

                            if r.get('CC', {}).get('value') and r.get('CCL', {}).get('value'):

                                for idx, (Id, label) in enumerate(zip(r['CC']['value'].split(' <|> '),r['CCL']['value'].split(' <|> '))):
                                    for k, math_form in answers['MathematicalFormulation'].items():
                                        if math_form.get('MathModID') == Id:
                                            math_form.setdefault('Relation1', {}).update({f'cc{idx}': option['ContainedAsConstraintConditionIn']})
                                            math_form.setdefault('Other1', {}).update({f'cc{idx}': f"{answers['AdditionalModel'][key]['MathModID']} <|> {answers['AdditionalModel'][key]['Name']}"})
                                            break
                                    else:  # This else corresponds to the for loop, it runs if the loop is not broken
                                        if answers['MathematicalFormulation'].keys():
                                            new_key = max(answers['MathematicalFormulation'].keys())+1 
                                        else:
                                            new_key = 0
                                        answers['MathematicalFormulation'].setdefault(new_key, {}).update({'MathModID': Id, 'Name': label})
                                        new_form = answers['MathematicalFormulation'][new_key]
                                        new_form.setdefault('Relation1', {}).update({f'cc{idx}': option['ContainedAsConstraintConditionIn']})
                                        new_form.setdefault('Other1', {}).update({f'cc{idx}': f"{answers['AdditionalModel'][key]['MathModID']} <|> {answers['AdditionalModel'][key]['Name']}"})
                            
                            if r.get('CPC', {}).get('value') and r.get('CPCL', {}).get('value'):

                                for idx, (Id, label) in enumerate(zip(r['CPC']['value'].split(' <|> '),r['CPCL']['value'].split(' <|> '))):
                                    for k, math_form in answers['MathematicalFormulation'].items():
                                        if math_form.get('MathModID') == Id:
                                            math_form.setdefault('Relation1', {}).update({f'cpc{idx}': option['ContainedAsCouplingConditionIn']})
                                            math_form.setdefault('Other1', {}).update({f'cpc{idx}': f"{answers['AdditionalModel'][key]['MathModID']} <|> {answers['AdditionalModel'][key]['Name']}"})
                                            break
                                    else:  # This else corresponds to the for loop, it runs if the loop is not broken
                                        if answers['MathematicalFormulation'].keys():
                                            new_key = max(answers['MathematicalFormulation'].keys())+1
                                        else:
                                            new_key = 0
                                        answers['MathematicalFormulation'].setdefault(new_key, {}).update({'MathModID': Id, 'Name': label})
                                        new_form = answers['MathematicalFormulation'][new_key]
                                        new_form.setdefault('Relation1', {}).update({f'cpc{idx}': option['ContainedAsCouplingConditionIn']})
                                        new_form.setdefault('Other1', {}).update({f'cpc{idx}': f"{answers['AdditionalModel'][key]['MathModID']} <|> {answers['AdditionalModel'][key]['Name']}"})

                            if r.get('IC', {}).get('value') and r.get('ICL', {}).get('value'):

                                for idx, (Id, label) in enumerate(zip(r['IC']['value'].split(' <|> '),r['ICL']['value'].split(' <|> '))):
                                    for k, math_form in answers['MathematicalFormulation'].items():
                                        if math_form.get('MathModID') == Id:
                                            math_form.setdefault('Relation1', {}).update({f'ic{idx}': option['ContainedAsInitialConditionIn']})
                                            math_form.setdefault('Other1', {}).update({f'ic{idx}': f"{answers['AdditionalModel'][key]['MathModID']} <|> {answers['AdditionalModel'][key]['Name']}"})
                                            break
                                    else:  # This else corresponds to the for loop, it runs if the loop is not broken
                                        if answers['MathematicalFormulation'].keys():
                                            new_key = max(answers['MathematicalFormulation'].keys())+1 
                                        else:
                                            new_key = 0
                                        answers['MathematicalFormulation'].setdefault(new_key, {}).update({'MathModID': Id, 'Name': label})
                                        new_form = answers['MathematicalFormulation'][new_key]
                                        new_form.setdefault('Relation1', {}).update({f'ic{idx}': option['ContainedAsInitialConditionIn']})
                                        new_form.setdefault('Other1', {}).update({f'ic{idx}': f"{answers['AdditionalModel'][key]['MathModID']} <|> {answers['AdditionalModel'][key]['Name']}"})

                            if r.get('FC', {}).get('value') and r.get('FCL', {}).get('value'):

                                for idx, (Id, label) in enumerate(zip(r['FC']['value'].split(' <|> '),r['FCL']['value'].split(' <|> '))):
                                    for k, math_form in answers['MathematicalFormulation'].items():
                                        if math_form.get('MathModID') == Id:
                                            math_form.setdefault('Relation1', {}).update({f'fc{idx}': option['ContainedAsFinalConditionIn']})
                                            math_form.setdefault('Other1', {}).update({f'fc{idx}': f"{answers['AdditionalModel'][key]['MathModID']} <|> {answers['AdditionalModel'][key]['Name']}"})
                                            break
                                    else:  # This else corresponds to the for loop, it runs if the loop is not broken
                                        if answers['MathematicalFormulation'].keys():
                                            new_key = max(answers['MathematicalFormulation'].keys())+1 
                                        else:
                                            new_key = 0
                                        answers['MathematicalFormulation'].setdefault(new_key, {}).update({'MathModID': Id, 'Name': label})
                                        new_form = answers['MathematicalFormulation'][new_key]
                                        new_form.setdefault('Relation1', {}).update({f'fc{idx}': option['ContainedAsFinalConditionIn']})
                                        new_form.setdefault('Other1', {}).update({f'fc{idx}': f"{answers['AdditionalModel'][key]['MathModID']} <|> {answers['AdditionalModel'][key]['Name']}"})

                        for r in req2:

                            if r.get('GBMODEL', {}).get('value') and r.get('GBMLabel', {}).get('value'):

                                for idx, (Id, label) in enumerate(zip(r['GBMODEL']['value'].split(' <|> '),r['GBMLabel']['value'].split(' <|> '))):
                                    answers['AdditionalModel'][key].setdefault('Relation1',{}).update({'gb'+str(idx):option['GeneralizedByModel']})
                                    answers['AdditionalModel'][key].setdefault('Other1',{}).update({'gb'+str(idx):Id + ' <|> ' + label})

                            elif r.get('GMODEL', {}).get('value') and r.get('GMLabel', {}).get('value'):

                                for idx, (Id, label) in enumerate(zip(r['GMODEL']['value'].split(' <|> '),r['GMLabel']['value'].split(' <|> '))):
                                    answers['AdditionalModel'][key].setdefault('Relation1',{}).update({'g'+str(idx):option['GeneralizesModel']})
                                    answers['AdditionalModel'][key].setdefault('Other1',{}).update({'g'+str(idx):Id + ' <|> ' + label})

                            elif r.get('ABMODEL', {}).get('value') and r.get('ABMLabel', {}).get('value'):

                                for idx, (Id, label) in enumerate(zip(r['ABMODEL']['value'].split(' <|> '),r['ABMLabel']['value'].split(' <|> '))):
                                    answers['AdditionalModel'][key].setdefault('Relation1',{}).update({'gb'+str(idx):option['ApproximatedByModel']})
                                    answers['AdditionalModel'][key].setdefault('Other1',{}).update({'gb'+str(idx):Id + ' <|> ' + label})

                            elif r.get('AMODEL', {}).get('value') and r.get('AMLabel', {}).get('value'):

                                for idx, (Id, label) in enumerate(zip(r['AMODEL']['value'].split(' <|> '),r['AMLabel']['value'].split(' <|> '))):
                                    answers['AdditionalModel'][key].setdefault('Relation1',{}).update({'a'+str(idx):option['ApproximatesModel']})
                                    answers['AdditionalModel'][key].setdefault('Other1',{}).update({'a'+str(idx):Id + ' <|> ' + label})

                            elif r.get('DBMODEL', {}).get('value') and r.get('DBMLabel', {}).get('value'):

                                for idx, (Id, label) in enumerate(zip(r['DBMODEL']['value'].split(' <|> '),r['DBMLabel']['value'].split(' <|> '))):
                                    answers['AdditionalModel'][key].setdefault('Relation1',{}).update({'db'+str(idx):option['DiscretizedByModel']})
                                    answers['AdditionalModel'][key].setdefault('Other1',{}).update({'db'+str(idx):Id + ' <|> ' + label})

                            elif r.get('DMODEL', {}).get('value') and r.get('DMLabel', {}).get('value'):

                                for idx, (Id, label) in enumerate(zip(r['DMODEL']['value'].split(' <|> '),r['DMLabel']['value'].split(' <|> '))):
                                    answers['AdditionalModel'][key].setdefault('Relation1',{}).update({'d'+str(idx):option['DiscretizesModel']})
                                    answers['AdditionalModel'][key].setdefault('Other1',{}).update({'d'+str(idx):Id + ' <|> ' + label})

                            elif r.get('LBMODEL', {}).get('value') and r.get('LBMLabel', {}).get('value'):

                                for idx, (Id, label) in enumerate(zip(r['LBMODEL']['value'].split(' <|> '),r['LBMLabel']['value'].split(' <|> '))):
                                    answers['AdditionalModel'][key].setdefault('Relation1',{}).update({'lb'+str(idx):option['LinearizedByModel']})
                                    answers['AdditionalModel'][key].setdefault('Other1',{}).update({'lb'+str(idx):Id + ' <|> ' + label})

                            elif r.get('LMODEL', {}).get('value') and r.get('LMLabel', {}).get('value'):

                                for idx, (Id, label) in enumerate(zip(r['LMODEL']['value'].split(' <|> '),r['LMLabel']['value'].split(' <|> '))):
                                    answers['AdditionalModel'][key].setdefault('Relation1',{}).update({'d'+str(idx):option['LinearizesModel']})
                                    answers['AdditionalModel'][key].setdefault('Other1',{}).update({'d'+str(idx):Id + ' <|> ' + label})

                            elif r.get('SMODEL', {}).get('value') and r.get('SMLabel', {}).get('value'):

                                for idx, (Id, label) in enumerate(zip(r['SMODEL']['value'].split(' <|> '),r['SMLabel']['value'].split(' <|> '))):
                                    answers['AdditionalModel'][key].setdefault('Relation1',{}).update({'s'+str(idx):option['SimilarToModel']})
                                    answers['AdditionalModel'][key].setdefault('Other1',{}).update({'s'+str(idx):Id + ' <|> ' + label})
 
                # Get additional Task Information

                search_string = ''
                
                for key in answers['Task']:
                    if answers['Task'][key]['MathModID'] and answers['Task'][key]['MathModID'] != 'not in MathModDB':

                        search_string = search_string + f' :{answers["Task"][key]["MathModID"].split("#")[1]}'

                req=requests.get('https://sparql.ta4.m1.mardi.ovh/mathalgodb/query',
                                 params = {'format': 'json', 'query': query_ta.format(search_string)},
                                 headers = {'User-Agent': 'MaRDMO_0.1 (https://zib.de; reidelbach@zib.de)'}).json()['results']['bindings']

                req2=requests.get('https://sparql.ta4.m1.mardi.ovh/mathalgodb/query',
                                  params = {'format': 'json', 'query': query_ta2.format(search_string)},
                                  headers = {'User-Agent': 'MaRDMO_0.1 (https://zib.de; reidelbach@zib.de)'}).json()['results']['bindings']
                
                if req:
                    for r in req:
                        for key in answers['Task']:
                            if r.get('t', {}).get('value') == answers['Task'][key]['MathModID']:

                                if r.get('quote', {}).get('value'):
                                    answers['Task'][key].update({'Description':r['quote']['value']})
                                
                                if r.get('linear', {}):
                                    if r['linear']['value'] == 'true':
                                        answers['Task'][key].setdefault('Properties', {}).update({0:option['IsLinear']})
                                    else:
                                        answers['Task'][key].setdefault('Properties', {}).update({1:option['IsNotLinear']})
                                
                                if r.get('P', {}).get('value') and r.get('PL', {}).get('value'):
                                    for idx, (Id, label) in enumerate(zip(r['P']['value'].split(' <|> '),r['PL']['value'].split(' <|> '))):
                                        answers['Task'][key].setdefault('ResearchProblem',{}).update({'p'+str(idx):Id + ' <|> ' + label})
                                if r.get('subclass', {}).get('value'):
                                    answers['Task'][key].setdefault('TaskClass',{}).update({0:option[r['subclass']['value'].split('#')[-1]]})
                                
                                if r.get('F', {}).get('value') and r.get('FL', {}).get('value'):
                            
                                    for idx, (Id, label) in enumerate(zip(r['F']['value'].split(' <|> '),r['FL']['value'].split(' <|> '))):
                                        for k, math_form in answers['MathematicalFormulation'].items():
                                            if math_form.get('MathModID') == Id:
                                                math_form.setdefault('Relation4', {}).update({f'f{idx}': option['ContainedAsFormulationIn']})
                                                math_form.setdefault('Other4', {}).update({f'f{idx}': f"{answers['Task'][key]['MathModID']} <|> {answers['Task'][key]['Name']}"})
                                                break
                                        else:  # This else corresponds to the for loop, it runs if the loop is not broken
                                            if answers['MathematicalFormulation'].keys():
                                                new_key = max(answers['MathematicalFormulation'].keys())+1 
                                            else:
                                                new_key = 0
                                            answers['MathematicalFormulation'].setdefault(new_key, {}).update({'MathModID': Id, 'Name': label})
                                            new_form = answers['MathematicalFormulation'][new_key]
                                            new_form.setdefault('Relation4', {}).update({f'f{idx}': option['ContainedAsFormulationIn']})
                                            new_form.setdefault('Other4', {}).update({f'f{idx}': f"{answers['Task'][key]['MathModID']} <|> {answers['Task'][key]['Name']}"})
                            
                                if r.get('A', {}).get('value') and r.get('AL', {}).get('value'):
                                
                                    for idx, (Id, label) in enumerate(zip(r['A']['value'].split(' <|> '),r['AL']['value'].split(' <|> '))):
                                        for k, math_form in answers['MathematicalFormulation'].items():
                                            if math_form.get('MathModID') == Id:
                                                math_form.setdefault('Relation4', {}).update({f'a{idx}': option['ContainedAsAssumptionIn']})
                                                math_form.setdefault('Other4', {}).update({f'a{idx}': f"{answers['Task'][key]['MathModID']} <|> {answers['Task'][key]['Name']}"})
                                                break
                                        else:  # This else corresponds to the for loop, it runs if the loop is not broken
                                            if answers['MathematicalFormulation'].keys():
                                                new_key = max(answers['MathematicalFormulation'].keys())+1 
                                            else:
                                                new_key = 0
                                            answers['MathematicalFormulation'].setdefault(new_key, {}).update({'MathModID': Id, 'Name': label})
                                            new_form = answers['MathematicalFormulation'][new_key]
                                            new_form.setdefault('Relation4', {}).update({f'a{idx}': option['ContainedAsAssumptionIn']})
                                            new_form.setdefault('Other4', {}).update({f'a{idx}': f"{answers['Task'][key]['MathModID']} <|> {answers['Task'][key]['Name']}"})

                                if r.get('BC', {}).get('value') and r.get('BCL', {}).get('value'):

                                    for idx, (Id, label) in enumerate(zip(r['BC']['value'].split(' <|> '),r['BCL']['value'].split(' <|> '))):
                                        for k, math_form in answers['MathematicalFormulation'].items():
                                            if math_form.get('MathModID') == Id:
                                                math_form.setdefault('Relation4', {}).update({f'bc{idx}': option['ContainedBoundaryConditionIn']})
                                                math_form.setdefault('Other4', {}).update({f'bc{idx}': f"{answers['Task'][key]['MathModID']} <|> {answers['Task'][key]['Name']}"})
                                                break
                                        else:  # This else corresponds to the for loop, it runs if the loop is not broken
                                            if answers['MathematicalFormulation'].keys():
                                                new_key = max(answers['MathematicalFormulation'].keys())+1 
                                            else:
                                                new_key = 0
                                            answers['MathematicalFormulation'].setdefault(new_key, {}).update({'MathModID': Id, 'Name': label})
                                            new_form = answers['MathematicalFormulation'][new_key]
                                            new_form.setdefault('Relation4', {}).update({f'bc{idx}': option['ContainedAsBoundaryConditionIn']})
                                            new_form.setdefault('Other4', {}).update({f'bc{idx}': f"{answers['Task'][key]['MathModID']} <|> {answers['Task'][key]['Name']}"})

                                if r.get('CC', {}).get('value') and r.get('CCL', {}).get('value'):
                            
                                    for idx, (Id, label) in enumerate(zip(r['CC']['value'].split(' <|> '),r['CCL']['value'].split(' <|> '))):
                                        for k, math_form in answers['MathematicalFormulation'].items():
                                            if math_form.get('MathModID') == Id:
                                                math_form.setdefault('Relation4', {}).update({f'cc{idx}': option['ContainedAsConstraintConditionIn']})
                                                math_form.setdefault('Other4', {}).update({f'cc{idx}': f"{answers['Task'][key]['MathModID']} <|> {answers['Task'][key]['Name']}"})
                                                break
                                        else:  # This else corresponds to the for loop, it runs if the loop is not broken
                                            if answers['MathematicalFormulation'].keys():
                                                new_key = max(answers['MathematicalFormulation'].keys())+1 
                                            else:
                                                new_key = 0
                                            answers['MathematicalFormulation'].setdefault(new_key, {}).update({'MathModID': Id, 'Name': label})
                                            new_form = answers['MathematicalFormulation'][new_key]
                                            new_form.setdefault('Relation4', {}).update({f'cc{idx}': option['ContainedAsConstraintConditionIn']})
                                            new_form.setdefault('Other4', {}).update({f'cc{idx}': f"{answers['Task'][key]['MathModID']} <|> {answers['Task'][key]['Name']}"})
                                
                                if r.get('CPC', {}).get('value') and r.get('CPCL', {}).get('value'):

                                    for idx, (Id, label) in enumerate(zip(r['CPC']['value'].split(' <|> '),r['CPCL']['value'].split(' <|> '))):
                                        for k, math_form in answers['MathematicalFormulation'].items():
                                            if math_form.get('MathModID') == Id:
                                                math_form.setdefault('Relation4', {}).update({f'cpc{idx}': option['ContainedAsCouplingConditionIn']})
                                                math_form.setdefault('Other4', {}).update({f'cpc{idx}': f"{answers['Task'][key]['MathModID']} <|> {answers['Task'][key]['Name']}"})
                                                break
                                        else:  # This else corresponds to the for loop, it runs if the loop is not broken
                                            if answers['MathematicalFormulation'].keys():
                                                new_key = max(answers['MathematicalFormulation'].keys())+1
                                            else:
                                                new_key = 0
                                            answers['MathematicalFormulation'].setdefault(new_key, {}).update({'MathModID': Id, 'Name': label})
                                            new_form = answers['MathematicalFormulation'][new_key]
                                            new_form.setdefault('Relation4', {}).update({f'cpc{idx}': option['ContainedAsCouplingConditionIn']})
                                            new_form.setdefault('Other4', {}).update({f'cpc{idx}': f"{answers['Task'][key]['MathModID']} <|> {answers['Task'][key]['Name']}"})

                                if r.get('IC', {}).get('value') and r.get('ICL', {}).get('value'):

                                    for idx, (Id, label) in enumerate(zip(r['IC']['value'].split(' <|> '),r['ICL']['value'].split(' <|> '))):
                                        for k, math_form in answers['MathematicalFormulation'].items():
                                            if math_form.get('MathModID') == Id:
                                                math_form.setdefault('Relation4', {}).update({f'ic{idx}': option['ContainedAsInitialConditionIn']})
                                                math_form.setdefault('Other4', {}).update({f'ic{idx}': f"{answers['Task'][key]['MathModID']} <|> {answers['Task'][key]['Name']}"})
                                                break
                                        else:  # This else corresponds to the for loop, it runs if the loop is not broken
                                            if answers['MathematicalFormulation'].keys():
                                                new_key = max(answers['MathematicalFormulation'].keys())+1 
                                            else:
                                                new_key = 0
                                            answers['MathematicalFormulation'].setdefault(new_key, {}).update({'MathModID': Id, 'Name': label})
                                            new_form = answers['MathematicalFormulation'][new_key]
                                            new_form.setdefault('Relation4', {}).update({f'ic{idx}': option['ContainedAsInitialConditionIn']})
                                            new_form.setdefault('Other4', {}).update({f'ic{idx}': f"{answers['Task'][key]['MathModID']} <|> {answers['Task'][key]['Name']}"})

                                if r.get('FC', {}).get('value') and r.get('FCL', {}).get('value'):

                                    for idx, (Id, label) in enumerate(zip(r['FC']['value'].split(' <|> '),r['FCL']['value'].split(' <|> '))):
                                        for k, math_form in answers['MathematicalFormulation'].items():
                                            if math_form.get('MathModID') == Id:
                                                math_form.setdefault('Relation4', {}).update({f'fc{idx}': option['ContainedAsFinalConditionIn']})
                                                math_form.setdefault('Other4', {}).update({f'fc{idx}': f"{answers['Task'][key]['MathModID']} <|> {answers['Task'][key]['Name']}"})
                                                break
                                        else:  # This else corresponds to the for loop, it runs if the loop is not broken
                                            if answers['MathematicalFormulation'].keys():
                                                new_key = max(answers['MathematicalFormulation'].keys())+1 
                                            else:
                                                new_key = 0
                                            answers['MathematicalFormulation'].setdefault(new_key, {}).update({'MathModID': Id, 'Name': label})
                                            new_form = answers['MathematicalFormulation'][new_key]
                                            new_form.setdefault('Relation4', {}).update({f'fc{idx}': option['ContainedAsFinalConditionIn']})
                                            new_form.setdefault('Other4', {}).update({f'fc{idx}': f"{answers['Task'][key]['MathModID']} <|> {answers['Task'][key]['Name']}"})

                                if r.get('IN', {}).get('value') and r.get('INL', {}).get('value') and r.get('INC', {}).get('value'):
                                
                                    for idx, (Id, label, Class) in enumerate(zip(r['IN']['value'].split(' <|> '),r['INL']['value'].split(' <|> '),r['INC']['value'].split(' <|> '))):
                                        if Class.split('#')[-1] == 'MathematicalFormulation': 
                                        
                                            for k, math_form in answers['MathematicalFormulation'].items():
                                                if math_form.get('MathModID') == Id:
                                                    math_form.setdefault('Relation4', {}).update({f'in{idx}': option['ContainedAsInput']})
                                                    math_form.setdefault('Other4', {}).update({f'in{idx}': f"{answers['Task'][key]['MathModID']} <|> {answers['Task'][key]['Name']}"})
                                                    break
                                            else:  # This else corresponds to the for loop, it runs if the loop is not broken
                                                if answers['MathematicalFormulation'].keys():
                                                    new_key = max(answers['MathematicalFormulation'].keys())+1 
                                                else:
                                                    new_key = 0
                                                answers['MathematicalFormulation'].setdefault(new_key, {}).update({'MathModID': Id, 'Name': label})
                                                new_form = answers['MathematicalFormulation'][new_key]
                                                new_form.setdefault('Relation4', {}).update({f'in{idx}': option['ContainedAsInputIn']})
                                                new_form.setdefault('Other4', {}).update({f'in{idx}': f"{answers['Task'][key]['MathModID']} <|> {answers['Task'][key]['Name']}"})
                                    
                                        elif Class.split('#')[-1] == 'Quantity' or Class.split('#')[-1] == 'QuantityKind':
                                            answers['Task'][key].setdefault('Relation2',{}).update({'in'+str(idx):option['ContainsInput']})
                                            if Class.split('#')[-1] == 'Quantity':
                                                answers['Task'][key].setdefault('Other2',{}).update({'in'+str(idx):Id + ' <|> ' + label + ' (Quantity)'})
                                            else:
                                                answers['Task'][key].setdefault('Other2',{}).update({'in'+str(idx):Id + ' <|> ' + label + ' (QuantityKind)'})
                            
                                if r.get('O', {}).get('value') and r.get('OL', {}).get('value') and r.get('OC', {}).get('value'):
                                
                                    for idx, (Id, label, Class) in enumerate(zip(r['O']['value'].split(' <|> '),r['OL']['value'].split(' <|> '),r['OC']['value'].split(' <|> '))):
                                        if Class.split('#')[-1] == 'MathematicalFormulation':
                                        
                                            for k, math_form in answers['MathematicalFormulation'].items():
                                                if math_form.get('MathModID') == Id:
                                                    math_form.setdefault('Relation4', {}).update({f'out{idx}': option['ContainedAsOutputIn']})
                                                    math_form.setdefault('Other4', {}).update({f'out{idx}': f"{answers['Task'][key]['MathModID']} <|> {answers['Task'][key]['Name']}"})
                                                    break
                                            else:  # This else corresponds to the for loop, it runs if the loop is not broken
                                                if answers['MathematicalFormulation'].keys():
                                                    new_key = max(answers['MathematicalFormulation'].keys())+1 
                                                else:
                                                    new_key = 0
                                                answers['MathematicalFormulation'].setdefault(new_key, {}).update({'MathModID': Id, 'Name': label})
                                                new_form = answers['MathematicalFormulation'][new_key]
                                                new_form.setdefault('Relation4', {}).update({f'out{idx}': option['ContainedAsOutputIn']})
                                                new_form.setdefault('Other4', {}).update({f'out{idx}': f"{answers['Task'][key]['MathModID']} <|> {answers['Task'][key]['Name']}"})
                                    
                                        elif Class.split('#')[-1] == 'Quantity' or Class.split('#')[-1] == 'QuantityKind':
                                            answers['Task'][key].setdefault('Relation2',{}).update({'out'+str(idx):option['ContainsOutput']})
                                            if Class.split('#')[-1] == 'Quantity':
                                                answers['Task'][key].setdefault('Other2',{}).update({'out'+str(idx):Id + ' <|> ' + label + ' (Quantity)'})
                                            else:
                                                answers['Task'][key].setdefault('Other2',{}).update({'out'+str(idx):Id + ' <|> ' + label + ' (QuantityKind)'})
                            
                                if r.get('OB', {}).get('value') and r.get('OBL', {}).get('value') and r.get('OBCl', {}).get('value'):
                                
                                    for idx, (Id, label, Class) in enumerate(zip(r['OB']['value'].split(' <|> '),r['OBL']['value'].split(' <|> '),r['OBC']['value'].split(' <|> '))):
                                        if Class.split('#')[-1] == 'MathematicalFormulation':
                                        
                                            for k, math_form in answers['MathematicalFormulation'].items():
                                                if math_form.get('MathModID') == Id:
                                                    math_form.setdefault('Relation4', {}).update({f'obj{idx}': option['ContainedAsObjectiveIn']})
                                                    math_form.setdefault('Other4', {}).update({f'obj{idx}': f"{answers['Task'][key]['MathModID']} <|> {answers['Task'][key]['Name']}"})
                                                    break
                                            else:  # This else corresponds to the for loop, it runs if the loop is not broken
                                                if answers['MathematicalFormulation'].keys():
                                                    new_key = max(answers['MathematicalFormulation'].keys())+1 
                                                else:
                                                    new_key = 0
                                                answers['MathematicalFormulation'].setdefault(new_key, {}).update({'MathModID': Id, 'Name': label})
                                                new_form = answers['MathematicalFormulation'][new_key]
                                                new_form.setdefault('Relation4', {}).update({f'obj{idx}': option['ContainedAsObjectiveIn']})
                                                new_form.setdefault('Other4', {}).update({f'obj{idx}': f"{answers['Task'][key]['MathModID']} <|> {answers['Task'][key]['Name']}"})

                                        elif Class.split('#')[-1] == 'Quantity' or Class.split('#')[-1] == 'QuantityKind':
                                            answers['Task'][key].setdefault('Relation2',{}).update({'obj'+str(idx):option['ContainsObjective']})
                                            if Class.split('#')[-1] == 'Quantity':
                                                answers['Task'][key].setdefault('Other2',{}).update({'obj'+str(idx):Id + ' <|> ' + label + ' (Quantity)'})
                                            else:
                                                answers['Task'][key].setdefault('Other2',{}).update({'obj'+str(idx):Id + ' <|> ' + label + ' (QuantityKind)'})

                                if r.get('PA', {}).get('value') and r.get('PAL', {}).get('value') and r.get('PAC', {}).get('value'):
                                
                                    for idx, (Id, label, Class) in enumerate(zip(r['PA']['value'].split(' <|> '),r['PAL']['value'].split(' <|> '),r['PAC']['value'].split(' <|> '))):
                                        if Class.split('#')[-1] == 'MathematicalFormulation':

                                            for k, math_form in answers['MathematicalFormulation'].items():
                                                if math_form.get('MathModID') == Id:
                                                    math_form.setdefault('Relation4', {}).update({f'pa{idx}': option['ContainedAsParameterIn']})
                                                    math_form.setdefault('Other4', {}).update({f'pa{idx}': f"{answers['Task'][key]['MathModID']} <|> {answers['Task'][key]['Name']}"})
                                                    break
                                            else:  # This else corresponds to the for loop, it runs if the loop is not broken
                                                if answers['MathematicalFormulation'].keys():
                                                    new_key = max(answers['MathematicalFormulation'].keys())+1 
                                                else:
                                                    new_key = 0
                                                answers['MathematicalFormulation'].setdefault(new_key, {}).update({'MathModID': Id, 'Name': label})
                                                new_form = answers['MathematicalFormulation'][new_key]
                                                new_form.setdefault('Relation4', {}).update({f'pa{idx}': option['ContainedAsParameterIn']})
                                                new_form.setdefault('Other4', {}).update({f'pa{idx}': f"{answers['Task'][key]['MathModID']} <|> {answers['Task'][key]['Name']}"})

                                        elif Class.split('#')[-1] == 'Quantity' or Class.split('#')[-1] == 'QuantityKind':
                                            answers['Task'][key].setdefault('Relation2',{}).update({'pa'+str(idx):option['ContainsParameter']})
                                            if Class.split('#')[-1] == 'Quantity':
                                                answers['Task'][key].setdefault('Other2',{}).update({'pa'+str(idx):Id + ' <|> ' + label + ' (Quantity)'})
                                            else:
                                                answers['Task'][key].setdefault('Other2',{}).update({'pa'+str(idx):Id + ' <|> ' + label + ' (QuantityKind)'})
                
                if req2:

                    for r in req2:
                        for key in answers['Task']:
                            if r.get('t', {}).get('value') == answers['Task'][key]['MathModID']:
                            
                                if r.get('GBTASK', {}).get('value') and r.get('GBTLabel', {}).get('value'):
                                
                                    for idx, (Id, label) in enumerate(zip(r['GBTASK']['value'].split(' <|> '),r['GBTLabel']['value'].split(' <|> '))):
                                        answers['Task'][key].setdefault('Relation3',{}).update({'gb'+str(idx):option['GeneralizedByTask']})
                                        answers['Task'][key].setdefault('Other3',{}).update({'gb'+str(idx):Id + ' <|> ' + label})

                                elif r.get('GTASK', {}).get('value') and r.get('GTLabel', {}).get('value'):

                                    for idx, (Id, label) in enumerate(zip(r['GTASK']['value'].split(' <|> '),r['GTLabel']['value'].split(' <|> '))):
                                        answers['Task'][key].setdefault('Relation3',{}).update({'g'+str(idx):option['GeneralizesTask']})
                                        answers['Task'][key].setdefault('Other3',{}).update({'g'+str(idx):Id + ' <|> ' + label})

                                elif r.get('ABTASK', {}).get('value') and r.get('ABTLabel', {}).get('value'):

                                    for idx, (Id, label) in enumerate(zip(r['ABTASK']['value'].split(' <|> '),r['ABTLabel']['value'].split(' <|> '))):
                                        answers['Task'][key].setdefault('Relation3',{}).update({'gb'+str(idx):option['ApproximatedByTask']})
                                        answers['Task'][key].setdefault('Other3',{}).update({'gb'+str(idx):Id + ' <|> ' + label})

                                elif r.get('ATASK', {}).get('value') and r.get('ATLabel', {}).get('value'):

                                    for idx, (Id, label) in enumerate(zip(r['ATASK']['value'].split(' <|> '),r['ATLabel']['value'].split(' <|> '))):
                                        answers['Task'][key].setdefault('Relation3',{}).update({'a'+str(idx):option['ApproximatesTask']})
                                        answers['Task'][key].setdefault('Other3',{}).update({'a'+str(idx):Id + ' <|> ' + label})

                                elif r.get('DBTASK', {}).get('value') and r.get('DBTLabel', {}).get('value'):

                                    for idx, (Id, label) in enumerate(zip(r['DBTASK']['value'].split(' <|> '),r['DBTLabel']['value'].split(' <|> '))):
                                        answers['Task'][key].setdefault('Relation3',{}).update({'db'+str(idx):option['DiscretizedByTask']})
                                        answers['Task'][key].setdefault('Other3',{}).update({'db'+str(idx):Id + ' <|> ' + label})

                                elif r.get('DTASK', {}).get('value') and r.get('DTLabel', {}).get('value'):

                                    for idx, (Id, label) in enumerate(zip(r['DTASK']['value'].split(' <|> '),r['DTLabel']['value'].split(' <|> '))):
                                        answers['Task'][key].setdefault('Relation3',{}).update({'d'+str(idx):option['DiscretizesTask']})
                                        answers['Task'][key].setdefault('Other3',{}).update({'d'+str(idx):Id + ' <|> ' + label})

                                elif r.get('LBTASK', {}).get('value') and r.get('LBTLabel', {}).get('value'):

                                    for idx, (Id, label) in enumerate(zip(r['LBTASK']['value'].split(' <|> '),r['LBTLabel']['value'].split(' <|> '))):
                                        answers['Task'][key].setdefault('Relation3',{}).update({'lb'+str(idx):option['LinearizedByTask']})
                                        answers['Task'][key].setdefault('Other3',{}).update({'lb'+str(idx):Id + ' <|> ' + label})

                                elif r.get('LTASK', {}).get('value') and r.get('LTLabel', {}).get('value'):

                                    for idx, (Id, label) in enumerate(zip(r['LTASK']['value'].split(' <|> '),r['LTLabel']['value'].split(' <|> '))):
                                        answers['Task'][key].setdefault('Relation3',{}).update({'l'+str(idx):option['LinearizesTask']})
                                        answers['Task'][key].setdefault('Other3',{}).update({'l'+str(idx):Id + ' <|> ' + label})

                                elif r.get('STASK', {}).get('value') and r.get('STLabel', {}).get('value'):

                                    for idx, (Id, label) in enumerate(zip(r['STASK']['value'].split(' <|> '),r['STLabel']['value'].split(' <|> '))):
                                        answers['Task'][key].setdefault('Relation3',{}).update({'s'+str(idx):option['SimilarToTask']})
                                        answers['Task'][key].setdefault('Other3',{}).update({'s'+str(idx):Id + ' <|> ' + label})
                
                # Get additional Mathematical Formulation Information
                if 'ID' in answers['Quantity'].get('MathModID',{}).keys():
                    del answers['Quantity']['MathModID']['ID']
                
                # Add Mathematical Formulation from Task to Formulation List
                for idx, key in enumerate(answers['Task']):
                    for key2 in answers['Task'][key].get('Relation1',{}):
                        
                        if answers['Task'][key]['Relation1'][key2] == option['ContainsAssumption']:
                            relation = option['ContainedAsAssumptionIn']
                        elif answers['Task'][key]['Relation1'][key2] == option['ContainsBoundaryCondition']:
                            relation = option['ContainedAsBoundaryConditionIn']
                        elif answers['Task'][key]['Relation1'][key2] == option['ContainsConstraintCondition']:
                            relation = option['ContainedAsConstraintConditionIn']
                        elif answers['Task'][key]['Relation1'][key2] == option['ContainsCouplingCondition']:
                            relation = option['ContainedAsCouplingConditionIn']
                        elif answers['Task'][key]['Relation1'][key2] == option['ContainsFormulation']:
                            relation = option['ContainedAsFormulationIn']
                        elif answers['Task'][key]['Relation1'][key2] == option['ContainsInitialCondition']:
                            relation = option['ContainedAsInitialConditionIn']
                        elif answers['Task'][key]['Relation1'][key2] == option['ContainsFinalCondition']:
                            relation = option['ContainedAsFinalConditionIn']
                        elif answers['Task'][key]['Relation1'][key2] == option['ContainsInput']:
                            relation = option['ContainedAsInputIn']
                        elif answers['Task'][key]['Relation1'][key2] == option['ContainsOutput']:
                            relation = option['ContainedAsOutputIn']
                        elif answers['Task'][key]['Relation1'][key2] == option['ContainsObjective']:
                            relation = option['ContainedAsObjectiveIn']
                        elif answers['Task'][key]['Relation1'][key2] == option['ContainsParameter']:
                            relation = option['ContainedAsParameterIn']

                        Id,label = answers['Task'][key]['Other1'][key2].split(' <|> ')[:2]
                        for k in answers['MathematicalFormulation']:
                            if label == answers['MathematicalFormulation'][k]['Name']:
                                answers['MathematicalFormulation'][k].setdefault('Relation4',{}).update({'abc'+str(key)+str(idx):relation})
                                answers['MathematicalFormulation'][k].setdefault('Other4',{}).update({'abc'+str(key)+str(idx):f"{answers['Task'][key]['MathModID']} <|> {answers['Task'][key]['Name']}"})
                                break
                        else:
                            if answers['MathematicalFormulation'].keys():
                                key3 = max(answers['MathematicalFormulation'].keys()) + 1
                            else:
                                key3 = 0
                            answers['MathematicalFormulation'].update({key3:{'MathModID':Id,'Name':label,
                                                                            'Relation4':{'abc'+str(key)+str(idx):relation},
                                                                            'Other4':{'abc'+str(key)+str(idx):f"{answers['Task'][key]['MathModID']} <|> {answers['Task'][key]['Name']}"}}})

                search_string = ''

                for key in answers['MathematicalFormulation']:
                    if answers['MathematicalFormulation'][key]['MathModID'] and answers['MathematicalFormulation'][key]['MathModID'] != 'not in MathModDB':

                        search_string = search_string + f' :{answers["MathematicalFormulation"][key]["MathModID"].split("#")[1]}'
                
                req=requests.get('https://sparql.ta4.m1.mardi.ovh/mathalgodb/query',
                                 params = {'format': 'json', 'query': query_mf.format(search_string)},
                                 headers = {'User-Agent': 'MaRDMO_0.1 (https://zib.de; reidelbach@zib.de)'}).json()['results']['bindings']

                req2=requests.get('https://sparql.ta4.m1.mardi.ovh/mathalgodb/query',
                                  params = {'format': 'json', 'query': query_mf2.format(search_string)},
                                  headers = {'User-Agent': 'MaRDMO_0.1 (https://zib.de; reidelbach@zib.de)'}).json()['results']['bindings']

                if req:

                    for r in req:
                        for key in answers['MathematicalFormulation']:
                            
                            if r.get('mf', {}).get('value') == answers['MathematicalFormulation'][key]['MathModID']:

                                if r.get('quote', {}).get('value'):
                                    answers['MathematicalFormulation'][key].update({'Description':r['quote']['value']})

                                if r.get('convex',{}):
                                    if r['convex']['value'] == 'true':
                                        answers['MathematicalFormulation'][key].setdefault('Properties',{}).update({0:option['IsConvex']})
                                    else:
                                        answers['MathematicalFormulation'][key].setdefault('Properties',{}).update({1:option['IsNotConvex']})

                                if r.get('deterministic',{}):
                                    if r['deterministic']['value'] == 'true':
                                        answers['MathematicalFormulation'][key].setdefault('Properties',{}).update({2:option['IsDeterministic']})
                                    else:
                                        answers['MathematicalFormulation'][key].setdefault('Properties',{}).update({3:option['IsStochastic']})
                            
                                if r.get('dimensionless',{}):
                                    if r['dimensionless']['value'] == 'true':
                                        answers['MathematicalFormulation'][key].setdefault('Properties',{}).update({4:option['IsDimensionless']})
                                    else:
                                        answers['MathematicalFormulation'][key].setdefault('Properties',{}).update({5:option['IsDimensional']})
                            
                                if r.get('dynamic',{}):
                                    if r['dynamic']['value'] == 'true':
                                        answers['MathematicalFormulation'][key].setdefault('Properties',{}).update({6:option['IsDynamic']})
                                    else:
                                        answers['MathematicalFormulation'][key].setdefault('Properties',{}).update({7:option['IsStatic']})
                            
                                if r.get('linear',{}):
                                    if r['linear']['value'] == 'true':
                                        answers['MathematicalFormulation'][key].setdefault('Properties',{}).update({8:option['IsLinear']})
                                    else:
                                        answers['MathematicalFormulation'][key].setdefault('Properties',{}).update({9:option['IsNotLinear']})
                            
                                if r.get('spacecont',{}):
                                    if r['spacecont']['value'] == 'true':
                                        answers['MathematicalFormulation'][key].setdefault('Properties',{}).update({10:option['IsSpaceContinuous']})
                                    else:
                                        answers['MathematicalFormulation'][key].setdefault('Properties',{}).update({11:option['IsSpaceDiscrete']})
                                else:
                                    answers['MathematicalFormulation'][key].setdefault('Properties',{}).update({12:option['IsSpaceIndependent']})
                            
                                if r.get('timecont',{}):
                                    if r['timecont']['value'] == 'true':
                                        answers['MathematicalFormulation'][key].setdefault('Properties',{}).update({13:option['IsTimeContinuous']})
                                    else:
                                        answers['MathematicalFormulation'][key].setdefault('Properties',{}).update({14:option['IsTimeDiscrete']})
                                else:
                                    answers['MathematicalFormulation'][key].setdefault('Properties',{}).update({15:option['IsTimeIndependent']})

                                if r.get('F', {}).get('value') and r.get('FL', {}).get('value'):
                                    for idx, (Id, label) in enumerate(zip(r['F']['value'].split(' <|> '),r['FL']['value'].split(' <|> '))):
                                        answers['MathematicalFormulation'][key].setdefault('Relation2', {}).update({f'fff{idx}': option['ContainsFormulation']})
                                        answers['MathematicalFormulation'][key].setdefault('Other2', {}).update({f'fff{idx}': f'{Id} <|> {label}'})
                            
                                if r.get('A', {}).get('value') and r.get('AL', {}).get('value'):
                                    for idx, (Id, label) in enumerate(zip(r['A']['value'].split(' <|> '),r['AL']['value'].split(' <|> '))):
                                        answers['MathematicalFormulation'][key].setdefault('Relation2', {}).update({f'aaa{idx}': option['ContainsAssumption']})
                                        answers['MathematicalFormulation'][key].setdefault('Other2', {}).update({f'aaa{idx}': f'{Id} <|> {label}'})

                                if r.get('BC', {}).get('value') and r.get('BCL', {}).get('value'):
                                    for idx, (Id, label) in enumerate(zip(r['BC']['value'].split(' <|> '),r['BCL']['value'].split(' <|> '))):
                                        answers['MathematicalFormulation'][key].setdefault('Relation2', {}).update({f'bcbcbc{idx}': option['ContainsBoundaryCondition']})
                                        answers['MathematicalFormulation'][key].setdefault('Other2', {}).update({f'bcbcbc{idx}': f'{Id} <|> {label}'})

                                if r.get('CC', {}).get('value') and r.get('CCL', {}).get('value'):
                                    for idx, (Id, label) in enumerate(zip(r['CC']['value'].split(' <|> '),r['CCL']['value'].split(' <|> '))):
                                        answers['MathematicalFormulation'][key].setdefault('Relation2', {}).update({f'cccccc{idx}': option['ContainsConstraintCondition']})
                                        answers['MathematicalFormulation'][key].setdefault('Other2', {}).update({f'cccccc{idx}': f'{Id} <|> {label}'})

                                if r.get('CPC', {}).get('value') and r.get('CPCL', {}).get('value'):
                                    for idx, (Id, label) in enumerate(zip(r['CPC']['value'].split(' <|> '),r['CPCL']['value'].split(' <|> '))):
                                        answers['MathematicalFormulation'][key].setdefault('Relation2', {}).update({f'cpccpccpc{idx}': option['ContainsCouplingCondition']})
                                        answers['MathematicalFormulation'][key].setdefault('Other2', {}).update({f'cpccpccpc{idx}': f'{Id} <|> {label}'})

                                if r.get('IC', {}).get('value') and r.get('ICL', {}).get('value'):
                                    for idx, (Id, label) in enumerate(zip(r['IC']['value'].split(' <|> '),r['ICL']['value'].split(' <|> '))):
                                        answers['MathematicalFormulation'][key].setdefault('Relation2', {}).update({f'icicic{idx}': option['ContainsInitialCondition']})
                                        answers['MathematicalFormulation'][key].setdefault('Other2', {}).update({f'icicic{idx}': f'{Id} <|> {label}'})

                                if r.get('FC', {}).get('value') and r.get('FCL', {}).get('value'):
                                    for idx, (Id, label) in enumerate(zip(r['FC']['value'].split(' <|> '),r['FCL']['value'].split(' <|> '))):
                                        answers['MathematicalFormulation'][key].setdefault('Relation2', {}).update({f'fcfcfc{idx}': option['ContainsFinalCondition']})
                                        answers['MathematicalFormulation'][key].setdefault('Other2', {}).update({f'fcfcfc{idx}': f'{Id} <|> {label}'})

                                if r.get('formula',{}).get('value'):
                                    for idx,formula in enumerate(r['formula']['value'].split(' <|> ')):
                                        answers['MathematicalFormulation'][key].setdefault('Formula',{}).update({idx:'$'+formula+'$'})
                            
                                if r.get('formula_elements',{}).get('value'):
                                    for idx,element in enumerate(r['formula_elements']['value'].split(' <|> ')):
                                        answers['MathematicalFormulation'][key].setdefault('Element',{}).update({idx:{'Symbol':'$'+element.split(',')[0]+'$','Quantity':element.split(',')[-1].lstrip()}})
                            
                                if r.get('quantity', {}).get('value') and r.get('quantityLabel', {}).get('value') and r.get('QC', {}).get('value'):
                                    for idx, (Id, label, Class) in enumerate(zip(r['quantity']['value'].split(' <|> '), r['quantityLabel']['value'].split(' <|> '),r['QC']['value'].split(' <|> '))):
                                        for k in answers['Quantity']['MathModID']:
                                            if answers['Quantity']['MathModID'][k] == f'{Id} <|> {label} ({Class.split("#")[1]})':
                                                break
                                        else:
                                            if answers['Quantity']['MathModID'].keys():
                                                val = max(answers['Quantity']['MathModID'].keys())+1
                                            else:
                                                val = 0
                                            answers['Quantity']['MathModID'].update({val:f'{Id} <|> {label} ({Class.split("#")[1]})'})

                if req2:

                    for r in req2:
                        for key in answers['MathematicalFormulation']:
                            if r.get('mf', {}).get('value') == answers['MathematicalFormulation'][key]['MathModID']:

                                if r.get('GBFORMULA', {}).get('value') and r.get('GBFLabel', {}).get('value'):

                                    for idx, (Id, label) in enumerate(zip(r['GBFORMULA']['value'].split(' <|> '),r['GBFLabel']['value'].split(' <|> '))):
                                        answers['MathematicalFormulation'][key].setdefault('Relation3',{}).update({'gb'+str(idx):option['GeneralizedByFormulation']})
                                        answers['MathematicalFormulation'][key].setdefault('Other3',{}).update({'gb'+str(idx):Id + ' <|> ' + label})

                                elif r.get('GFORMULA', {}).get('value') and r.get('GFLabel', {}).get('value'):

                                    for idx, (Id, label) in enumerate(zip(r['GFORMULA']['value'].split(' <|> '),r['GFLabel']['value'].split(' <|> '))):
                                        answers['MathematicalFormulation'][key].setdefault('Relation3',{}).update({'g'+str(idx):option['GeneralizesFormulation']})
                                        answers['MathematicalFormulation'][key].setdefault('Other3',{}).update({'g'+str(idx):Id + ' <|> ' + label})

                                elif r.get('ABFORMULA', {}).get('value') and r.get('ABFLabel', {}).get('value'):

                                    for idx, (Id, label) in enumerate(zip(r['ABFORMULA']['value'].split(' <|> '),r['ABFLabel']['value'].split(' <|> '))):
                                        answers['MathematicalFormulation'][key].setdefault('Relation3',{}).update({'ab'+str(idx):option['ApproximatedByFormulation']})
                                        answers['MathematicalFormulation'][key].setdefault('Other3',{}).update({'ab'+str(idx):Id + ' <|> ' + label})

                                elif r.get('AFORMULA', {}).get('value') and r.get('AFLabel', {}).get('value'):

                                    for idx, (Id, label) in enumerate(zip(r['AFORMULA']['value'].split(' <|> '),r['AFLabel']['value'].split(' <|> '))):
                                        answers['MathematicalFormulation'][key].setdefault('Relation3',{}).update({'a'+str(idx):option['ApproximatesFormulation']})
                                        answers['MathematicalFormulation'][key].setdefault('Other3',{}).update({'a'+str(idx):Id + ' <|> ' + label})

                                elif r.get('DBFORMULA', {}).get('value') and r.get('DBFLabel', {}).get('value'):

                                    for idx, (Id, label) in enumerate(zip(r['DBFORMULA']['value'].split(' <|> '),r['DBFLabel']['value'].split(' <|> '))):
                                        answers['MathematicalFormulation'][key].setdefault('Relation3',{}).update({'db'+str(idx):option['DiscretizedByFormulation']})
                                        answers['MathematicalFormulation'][key].setdefault('Other3',{}).update({'db'+str(idx):Id + ' <|> ' + label})

                                elif r.get('DFORMULA', {}).get('value') and r.get('DFLabel', {}).get('value'):

                                    for idx, (Id, label) in enumerate(zip(r['DFORMULA']['value'].split(' <|> '),r['DFLabel']['value'].split(' <|> '))):
                                        answers['MathematicalFormulation'][key].setdefault('Relation3',{}).update({'d'+str(idx):option['DiscretizesFormulation']})
                                        answers['MathematicalFormulation'][key].setdefault('Other3',{}).update({'d'+str(idx):Id + ' <|> ' + label})

                                elif r.get('LBFORMULA', {}).get('value') and r.get('LBFLabel', {}).get('value'):

                                    for idx, (Id, label) in enumerate(zip(r['LBFORMULA']['value'].split(' <|> '),r['LBFLabel']['value'].split(' <|> '))):
                                        answers['MathematicalFormulation'][key].setdefault('Relation3',{}).update({'lb'+str(idx):option['LinearizedByFormulation']})
                                        answers['MathematicalFormulation'][key].setdefault('Other3',{}).update({'lb'+str(idx):Id + ' <|> ' + label})

                                elif r.get('LFORMULA', {}).get('value') and r.get('LFLabel', {}).get('value'):

                                    for idx, (Id, label) in enumerate(zip(r['LFORMULA']['value'].split(' <|> '),r['LFLabel']['value'].split(' <|> '))):
                                        answers['MathematicalFormulation'][key].setdefault('Relation3',{}).update({'l'+str(idx):option['LinearizesFormulation']})
                                        answers['MathematicalFormulation'][key].setdefault('Other3',{}).update({'l'+str(idx):Id + ' <|> ' + label})
                                
                                elif r.get('NBFORMULA', {}).get('value') and r.get('NBFLabel', {}).get('value'):

                                    for idx, (Id, label) in enumerate(zip(r['NBFORMULA']['value'].split(' <|> '),r['NBFLabel']['value'].split(' <|> '))):
                                        answers['MathematicalFormulation'][key].setdefault('Relation3',{}).update({'nb'+str(idx):option['NondimensionalizedByFormulation']})
                                        answers['MathematicalFormulation'][key].setdefault('Other3',{}).update({'nb'+str(idx):Id + ' <|> ' + label})

                                elif r.get('NFORMULA', {}).get('value') and r.get('NFLabel', {}).get('value'):

                                    for idx, (Id, label) in enumerate(zip(r['NFORMULA']['value'].split(' <|> '),r['NFLabel']['value'].split(' <|> '))):
                                        answers['MathematicalFormulation'][key].setdefault('Relation3',{}).update({'n'+str(idx):option['NondimensionalizesFormulation']})
                                        answers['MathematicalFormulation'][key].setdefault('Other3',{}).update({'n'+str(idx):Id + ' <|> ' + label})

                                elif r.get('SFORMULA', {}).get('value') and r.get('SFLabel', {}).get('value'):

                                    for idx, (Id, label) in enumerate(zip(r['SFORMULA']['value'].split(' <|> '),r['SFLabel']['value'].split(' <|> '))):
                                        answers['MathematicalFormulation'][key].setdefault('Relation3',{}).update({'s'+str(idx):option['SimilarToFormulation']})
                                        answers['MathematicalFormulation'][key].setdefault('Other3',{}).update({'s'+str(idx):Id + ' <|> ' + label})

                # Get additional Quantity Information

                search_string_q = ''
                search_string_qk = ''

                for key in answers['Quantity'].get('MathModID',{}):
                    
                    Id,label_qqk = answers['Quantity']['MathModID'][key].split(' <|> ')
                    label,qqk = label_qqk.rsplit(' ',1)
                    
                    if qqk == '(Quantity)':
                        search_string_q = search_string_q + f' :{Id.split("#")[1]}'
                    elif qqk == '(QuantityKind)':
                        search_string_qk = search_string_qk + f' :{Id.split("#")[1]}'
                 
                req_q  = requests.get('https://sparql.ta4.m1.mardi.ovh/mathalgodb/query',
                                      params = {'format': 'json', 'query': query_q.format(search_string_q)},
                                      headers = {'User-Agent': 'MaRDMO_0.1 (https://zib.de; reidelbach@zib.de)'}).json()['results']['bindings']

                req_q2  = requests.get('https://sparql.ta4.m1.mardi.ovh/mathalgodb/query',
                                       params = {'format': 'json', 'query': query_q2.format(search_string_q)},
                                       headers = {'User-Agent': 'MaRDMO_0.1 (https://zib.de; reidelbach@zib.de)'}).json()['results']['bindings']
                
                req_q3  = requests.get('https://sparql.ta4.m1.mardi.ovh/mathalgodb/query',
                                       params = {'format': 'json', 'query': query_q3.format(search_string_q)},
                                       headers = {'User-Agent': 'MaRDMO_0.1 (https://zib.de; reidelbach@zib.de)'}).json()['results']['bindings']

                req_qk = requests.get('https://sparql.ta4.m1.mardi.ovh/mathalgodb/query',
                                      params = {'format': 'json', 'query': query_qk.format(search_string_qk)},
                                      headers = {'User-Agent': 'MaRDMO_0.1 (https://zib.de; reidelbach@zib.de)'}).json()['results']['bindings']
                
                req_qk2 = requests.get('https://sparql.ta4.m1.mardi.ovh/mathalgodb/query',
                                      params = {'format': 'json', 'query': query_qk2.format(search_string_qk)},
                                      headers = {'User-Agent': 'MaRDMO_0.1 (https://zib.de; reidelbach@zib.de)'}).json()['results']['bindings']

                if req_q:
                    for r in req_q:
                        for key in answers['Quantity']['MathModID']:
                            if r.get('q', {}).get('value') == answers['Quantity']['MathModID'][key].split(' <|> ')[0]:
                            
                                answers.setdefault('Quantity_refined',{}).update({key:{'MathModID':r.get('q',{}).get('value'),'QName':r.get('qlabel',{}).get('value')}})
                            
                                if r.get('qquote', {}).get('value'):
                                    answers['Quantity_refined'][key].update({'QDescription':r['qquote']['value']})
                            
                                if r.get('qdimensionless', {}):
                                    if r['qdimensionless']['value'] == 'true':
                                        answers['Quantity_refined'][key].setdefault('QProperties', {}).update({0:option['IsDimensionless']})
                                    else:
                                        answers['Quantity_refined'][key].setdefault('QProperties', {}).update({1:option['IsDimensional']})
                                if r.get('qlinear', {}):
                                    if r['qlinear']['value'] == 'ture':
                                        answers['Quantity_refined'][key].setdefault('QProperties', {}).update({2:option['IsLinear']})
                                    else:
                                        answers['Quantity_refined'][key].setdefault('QProperties', {}).update({3:option['IsNotLinear']})
                            
                                if r.get('answer', {}).get('value'):
                                    answers['Quantity_refined'][key].update({'QKID':r['answer']['value']})
                            
                                if r.get('qklabel', {}).get('value'):
                                    answers['Quantity_refined'][key].update({'QKName':r['qklabel']['value']})
                            
                                if r.get('qkquote', {}).get('value'):
                                    answers['Quantity_refined'][key].update({'QKDescription':r['qkquote']['value']})
                            
                                if r.get('qkdimensionless', {}):
                                    if r['qkdimensionless']['value'] == 'true':
                                        answers['Quantity_refined'][key].setdefault('QKProperties', {}).update({0:option['IsDimensionless']})
                                    else:
                                        answers['Quantity_refined'][key].setdefault('QKProperties', {}).update({0:option['IsDimensional']})
                
                if req_qk:
                    for r in req_qk:
                        for key in answers['Quantity']['MathModID']:
                            if r.get('qk', {}).get('value') == answers['Quantity']['MathModID'][key].split(' <|> ')[0]:

                                answers.setdefault('QuantityKind_refined',{}).update({key:{'MathModID':r.get('qk',{}).get('value'),'QKName':r.get('qklabel',{}).get('value')}})
                    
                                if r.get('qkquote', {}).get('value'):
                                    answers['QuantityKind_refined'][key].update({'QKDescription':r['qkquote']['value']})
                    
                                if r.get('qkdimensionless', {}):
                                    if r['qkdimensionless']['value'] == 'true':
                                        answers['QuantityKind_refined'][key].setdefault('QKProperties', {}).update({0:option['IsDimensional']})
                                    else:
                                        answers['QuantityKind_refined'][key].setdefault('QKProperties', {}).update({0:option['IsNotDimensional']})
                
                if req_q2:
                    for r in req_q2:
                        
                        if answers['MathematicalFormulation'].keys():
                            key = max(answers['MathematicalFormulation'].keys()) + 1
                        else:
                            key = 0
                        
                        answers['MathematicalFormulation'].setdefault(key,{}).update({'MathModID':r.get('mf', {}).get('value')})
                        answers['MathematicalFormulation'][key].update({'Name':r.get('label', {}).get('value')})
                        answers['MathematicalFormulation'][key].update({'DefinedQuantity':f'{r.get("q", {}).get("value")} <|> {r.get("qlabel", {}).get("value")}'}) 

                        if r.get('quote', {}).get('value'):
                            answers['MathematicalFormulation'][key].update({'Description':r['quote']['value']})

                        if r.get('convex',{}).get('value'):
                            answers['MathematicalFormulation'][key].setdefault('Properties',{}).update({0:'http://example.com/terms/options/MaRDI/MathematicalFormulation_property0'})
                        
                        if r.get('deterministic',{}).get('value'):
                            answers['MathematicalFormulation'][key].setdefault('Properties',{}).update({1:'http://example.com/terms/options/MaRDI/MathematicalFormulation_property1'})
                        
                        if r.get('dimensionless',{}).get('value'):
                            answers['MathematicalFormulation'][key].setdefault('Properties',{}).update({2:'http://example.com/terms/options/MaRDI/MathematicalFormulation_property2'})
                        
                        if r.get('dynamic',{}).get('value'):
                            answers['MathematicalFormulation'][key].setdefault('Properties',{}).update({3:'http://example.com/terms/options/MaRDI/MathematicalFormulation_property3'})
                        
                        if r.get('linear',{}).get('value'):
                            answers['MathematicalFormulation'][key].setdefault('Properties',{}).update({4:'http://example.com/terms/options/MaRDI/MathematicalFormulation_property4'})
                        
                        if r.get('spacecont',{}).get('value'):
                            answers['MathematicalFormulation'][key].setdefault('Properties',{}).update({5:'http://example.com/terms/options/MaRDI/MathematicalFormulation_property5'})
                        
                        if r.get('timecont',{}).get('value'):
                            answers['MathematicalFormulation'][key].setdefault('Properties',{}).update({6:'http://example.com/terms/options/MaRDI/MathematicalFormulation_property6'})

                        if r.get('formula_elements',{}).get('value'):
                            for idx,element in enumerate(r['formula_elements']['value'].split(' <|> ')):
                                answers['MathematicalFormulation'][key].setdefault('Element',{}).update({idx:{'Symbol':'$'+element.split(',')[0]+'$','Quantity':element.split(',')[-1].lstrip()}})

                        if r.get('quantity', {}).get('value') and r.get('quantityLabel', {}).get('value') and r.get('QC', {}).get('value'):
                            for idx, (Id, label, Class) in enumerate(zip(r['quantity']['value'].split(' <|> '), r['quantityLabel']['value'].split(' <|> '),r['QC']['value'].split(' <|> '))):
                                if Class.split('#')[1] == 'Quantity':
                                    for k in answers['Quantity_refined']:
                                        if answers['Quantity_refined'][k]['MathModID'] == Id:
                                            break
                                    else:
                                        answers['Quantity_refined'].update({max(answers['Quantity_refined'].keys())+1:{'MathModID':Id,'QName':label}})
                                elif Class.split('#')[1] == 'QuantityKind':
                                    for k in answers['QuantityKind_refined']:
                                        if answers['QuantityKind_refined'][k]['MathModID'] == Id:
                                            break
                                    else:
                                        answers['QuantityKind_refined'].update({max(answers['QuantityKind_refined'].keys())+1:{'MathModID':Id,'QName':label}})
                
                if req_q3:

                    for r in req_q3:
                        for key in answers['Quantity_refined']:
                            if r.get('q', {}).get('value') == answers['Quantity_refined'][key]['MathModID']:
                                
                                if r.get('GBQUANTITY', {}).get('value') and r.get('GBQLabel', {}).get('value') and r.get('GBCLASS', {}).get('value'):

                                    for idx, (Id, label, Class) in enumerate(zip(r['GBQUANTITY']['value'].split(' <|> '),r['GBQLabel']['value'].split(' <|> '),r['GBCLASS']['value'].split(' <|> '))):
                                        if Class.split('#')[1] == 'Quantity':
                                            answers['Quantity_refined'][key].setdefault('Relation1',{}).update({'gb'+str(idx):option['GeneralizedByQuantity']})
                                            answers['Quantity_refined'][key].setdefault('Other1',{}).update({'gb'+str(idx):Id + ' <|> ' + label})
                                        elif Class.split('#')[1] == 'QuantityKind':
                                            answers['Quantity_refined'][key].setdefault('Relation2',{}).update({'gb'+str(idx):option['GeneralizedByQuantityKind']})
                                            answers['Quantity_refined'][key].setdefault('Other2',{}).update({'gb'+str(idx):Id + ' <|> ' + label})

                                elif r.get('GQUANTITY', {}).get('value') and r.get('GQLabel', {}).get('value') and r.get('GCLASS', {}).get('value'):
                                    
                                    for idx, (Id, label, Class) in enumerate(zip(r['GQUANTITY']['value'].split(' <|> '),r['GQLabel']['value'].split(' <|> '),r['GCLASS']['value'].split(' <|> '))):
                                        if Class.split('#')[1] == 'Quantity':
                                            answers['Quantity_refined'][key].setdefault('Relation1',{}).update({'g'+str(idx):option['GeneralizesQuantity']})
                                            answers['Quantity_refined'][key].setdefault('Other1',{}).update({'g'+str(idx):Id + ' <|> ' + label})
                                        elif Class.split('#')[1] == 'QuantityKind':
                                            answers['Quantity_refined'][key].setdefault('Relation2',{}).update({'g'+str(idx):option['GeneralizesQuantityKind']})
                                            answers['Quantity_refined'][key].setdefault('Other2',{}).update({'g'+str(idx):Id + ' <|> ' + label})

                                elif r.get('ABQUANTITY', {}).get('value') and r.get('ABQLabel', {}).get('value') and r.get('ABCLASS', {}).get('value'):

                                    for idx, (Id, label, Class) in enumerate(zip(r['ABQUANTITY']['value'].split(' <|> '),r['ABQLabel']['value'].split(' <|> '),r['ABCLASS']['value'].split(' <|> '))):
                                        if Class.split('#')[1] == 'Quantity':
                                            answers['Quantity_refined'][key].setdefault('Relation1',{}).update({'ab'+str(idx):option['ApproximatedByQuantity']})
                                            answers['Quantity_refined'][key].setdefault('Other1',{}).update({'ab'+str(idx):Id + ' <|> ' + label})
                                        elif Class.split('#')[1] == 'QuantityKind':
                                            answers['Quantity_refined'][key].setdefault('Relation2',{}).update({'ab'+str(idx):option['ApproximatedByQuantityKind']})
                                            answers['Quantity_refined'][key].setdefault('Other2',{}).update({'ab'+str(idx):Id + ' <|> ' + label})

                                elif r.get('AQUANTITY', {}).get('value') and r.get('AQLabel', {}).get('value') and r.get('ACLASS', {}).get('value'):

                                    for idx, (Id, label, Class) in enumerate(zip(r['AQUANTITY']['value'].split(' <|> '),r['AQLabel']['value'].split(' <|> '),r['ACLASS']['value'].split(' <|> '))):
                                        if Class.split('#')[1] == 'Quantity':
                                            answers['Quantity_refined'][key].setdefault('Relation1',{}).update({'a'+str(idx):option['ApproximatesQuantity']})
                                            answers['Quantity_refined'][key].setdefault('Other1',{}).update({'a'+str(idx):Id + ' <|> ' + label})
                                        elif Class.split('#')[1] == 'QuantityKind':
                                            answers['Quantity_refined'][key].setdefault('Relation2',{}).update({'a'+str(idx):option['ApproximatesQuantityKind']})
                                            answers['Quantity_refined'][key].setdefault('Other2',{}).update({'a'+str(idx):Id + ' <|> ' + label})

                                elif r.get('LBQUANTITY', {}).get('value') and r.get('LBQLabel', {}).get('value') and r.get('LBCLASS', {}).get('value'):

                                    for idx, (Id, label, Class) in enumerate(zip(r['LBQUANTITY']['value'].split(' <|> '),r['LBQLabel']['value'].split(' <|> '),r['LBCLASS']['value'].split(' <|> '))):
                                        if Class.split('#')[1] == 'Quantity':
                                            answers['Quantity_refined'][key].setdefault('Relation1',{}).update({'lb'+str(idx):option['LinearizedByQuantity']})
                                            answers['Quantity_refined'][key].setdefault('Other1',{}).update({'lb'+str(idx):Id + ' <|> ' + label})
                                        elif Class.split('#')[1] == 'QuantityKind':
                                            answers['Quantity_refined'][key].setdefault('Relation2',{}).update({'lb'+str(idx):option['LinearizedByQuantityKind']})
                                            answers['Quantity_refined'][key].setdefault('Other2',{}).update({'lb'+str(idx):Id + ' <|> ' + label})

                                elif r.get('LQUANTITY', {}).get('value') and r.get('LQLabel', {}).get('value') and r.get('LCLASS', {}).get('value'):

                                    for idx, (Id, label, Class) in enumerate(zip(r['LQUANTITY']['value'].split(' <|> '),r['LQLabel']['value'].split(' <|> '),r['LCLASS']['value'].split(' <|> '))):
                                        if Class.split('#')[1] == 'Quantity':
                                            answers['Quantity_refined'][key].setdefault('Relation1',{}).update({'l'+str(idx):option['LinearizesQuantity']})
                                            answers['Quantity_refined'][key].setdefault('Other1',{}).update({'l'+str(idx):Id + ' <|> ' + label})
                                        elif Class.split('#')[1] == 'QuantityKind':
                                            answers['Quantity_refined'][key].setdefault('Relation2',{}).update({'l'+str(idx):option['LinearizesQuantityKind']})
                                            answers['Quantity_refined'][key].setdefault('Other2',{}).update({'l'+str(idx):Id + ' <|> ' + label})

                                elif r.get('NBQUANTITY', {}).get('value') and r.get('NBQLabel', {}).get('value') and r.get('NBCLASS', {}).get('value'):

                                    for idx, (Id, label, Class) in enumerate(zip(r['NBQUANTITY']['value'].split(' <|> '),r['NBQLabel']['value'].split(' <|> '),r['NBCLASS']['value'].split(' <|> '))):
                                        if Class.split('#')[1] == 'Quantity':
                                            answers['Quantity_refined'][key].setdefault('Relation1',{}).update({'nb'+str(idx):option['NondimensionalizedByQuantity']})
                                            answers['Quantity_refined'][key].setdefault('Other1',{}).update({'nb'+str(idx):Id + ' <|> ' + label})
                                        elif Class.split('#')[1] == 'QuantityKind':
                                            answers['Quantity_refined'][key].setdefault('Relation2',{}).update({'nb'+str(idx):option['NondimensionalizedByQuantityKind']})
                                            answers['Quantity_refined'][key].setdefault('Other2',{}).update({'nb'+str(idx):Id + ' <|> ' + label})

                                elif r.get('NQUANTITY', {}).get('value') and r.get('NQLabel', {}).get('value') and r.get('NCLASS', {}).get('value'):

                                    for idx, (Id, label, Class) in enumerate(zip(r['NQUANTITY']['value'].split(' <|> '),r['NQLabel']['value'].split(' <|> '),r['NCLASS']['value'].split(' <|> '))):
                                        if Class.split('#')[1] == 'Quantity':
                                            answers['Quantity_refined'][key].setdefault('Relation1',{}).update({'n'+str(idx):option['NondimensionalizesQuantity']})
                                            answers['Quantity_refined'][key].setdefault('Other1',{}).update({'n'+str(idx):Id + ' <|> ' + label})
                                        elif Class.split('#')[1] == 'QuantityKind':
                                            answers['Quantity_refined'][key].setdefault('Relation2',{}).update({'n'+str(idx):option['NondimensionalizesQuantityKind']})
                                            answers['Quantity_refined'][key].setdefault('Other2',{}).update({'n'+str(idx):Id + ' <|> ' + label})

                                elif r.get('SQUANTITY', {}).get('value') and r.get('SQLabel', {}).get('value') and r.get('SCLASS', {}).get('value'):

                                    for idx, (Id, label, Class) in enumerate(zip(r['SQUANTITY']['value'].split(' <|> '),r['SQLabel']['value'].split(' <|> '),r['SCLASS']['value'].split(' <|> '))):
                                        if Class.split('#')[1] == 'Quantity':
                                            answers['Quantity_refined'][key].setdefault('Relation1',{}).update({'s'+str(idx):option['SimilarToQuantity']})
                                            answers['Quantity_refined'][key].setdefault('Other1',{}).update({'s'+str(idx):Id + ' <|> ' + label})
                                        elif Class.split('#')[1] == 'QuantityKind':
                                            answers['Quantity_refined'][key].setdefault('Relation2',{}).update({'s'+str(idx):option['SimilarToQuantityKind']})
                                            answers['Quantity_refined'][key].setdefault('Other2',{}).update({'s'+str(idx):Id + ' <|> ' + label})

                if req_qk2:

                    for r in req_qk2:
                        for key in answers.get('QuantityKind_refined',[]):
                            if r.get('q', {}).get('value') == answers['QuantityKind_refined'][key]['MathModID']:

                                if r.get('GBQUANTITY', {}).get('value') and r.get('GBQLabel', {}).get('value') and r.get('GBCLASS', {}).get('value'):

                                    for idx, (Id, label, Class) in enumerate(zip(r['GBQUANTITY']['value'].split(' <|> '),r['GBQLabel']['value'].split(' <|> '),r['GBCLASS']['value'].split(' <|> '))):
                                        if Class.split('#')[1] == 'Quantity':
                                            answers['QuantityKind_refined'][key].setdefault('Relation2',{}).update({'gb'+str(idx):option['GeneralizedByQuantity']})
                                            answers['QuantityKind_refined'][key].setdefault('Other2',{}).update({'gb'+str(idx):Id + ' <|> ' + label})
                                        elif Class.split('#')[1] == 'QuantityKind':
                                            answers['QuantityKind_refined'][key].setdefault('Relation1',{}).update({'gb'+str(idx):option['GeneralizedByQuantityKind']})
                                            answers['QuantityKind_refined'][key].setdefault('Other1',{}).update({'gb'+str(idx):Id + ' <|> ' + label})

                                elif r.get('GQUANTITY', {}).get('value') and r.get('GQLabel', {}).get('value') and r.get('GCLASS', {}).get('value'):

                                    for idx, (Id, label, Class) in enumerate(zip(r['GQUANTITY']['value'].split(' <|> '),r['GQLabel']['value'].split(' <|> '),r['GCLASS']['value'].split(' <|> '))):
                                        if Class.split('#')[1] == 'Quantity':
                                            answers['QuantityKind_refined'][key].setdefault('Relation2',{}).update({'g'+str(idx):option['GeneralizesQuantity']})
                                            answers['QuantityKind_refined'][key].setdefault('Other2',{}).update({'g'+str(idx):Id + ' <|> ' + label})
                                        elif Class.split('#')[1] == 'QuantityKind':
                                            answers['QuantityKind_refined'][key].setdefault('Relation1',{}).update({'g'+str(idx):option['GeneralizesQuantityKind']})
                                            answers['QuantityKind_refined'][key].setdefault('Other1',{}).update({'g'+str(idx):Id + ' <|> ' + label})
                                
                                elif r.get('NBQUANTITY', {}).get('value') and r.get('NBQLabel', {}).get('value') and r.get('NBCLASS', {}).get('value'):

                                    for idx, (Id, label, Class) in enumerate(zip(r['NBQUANTITY']['value'].split(' <|> '),r['NBQLabel']['value'].split(' <|> '),r['NBCLASS']['value'].split(' <|> '))):
                                        if Class.split('#')[1] == 'Quantity':
                                            answers['QuantityKind_refined'][key].setdefault('Relation2',{}).update({'nb'+str(idx):option['NondimensionalizedByQuantity']})
                                            answers['QuantityKind_refined'][key].setdefault('Other2',{}).update({'nb'+str(idx):Id + ' <|> ' + label})
                                        elif Class.split('#')[1] == 'QuantityKind':
                                            answers['QuantityKind_refined'][key].setdefault('Relation1',{}).update({'nb'+str(idx):option['NondimensionalizedByQuantityKind']})
                                            answers['QuantityKind_refined'][key].setdefault('Other1',{}).update({'nb'+str(idx):Id + ' <|> ' + label})

                                elif r.get('NQUANTITY', {}).get('value') and r.get('NQLabel', {}).get('value') and r.get('NCLASS', {}).get('value'):

                                    for idx, (Id, label, Class) in enumerate(zip(r['NQUANTITY']['value'].split(' <|> '),r['NQLabel']['value'].split(' <|> '),r['NCLASS']['value'].split(' <|> '))):
                                        if Class.split('#')[1] == 'Quantity':
                                            answers['QuantityKind_refined'][key].setdefault('Relation2',{}).update({'n'+str(idx):option['NondimensionalizesQuantity']})
                                            answers['QuantityKind_refined'][key].setdefault('Other2',{}).update({'n'+str(idx):Id + ' <|> ' + label})
                                        elif Class.split('#')[1] == 'QuantityKind':
                                            answers['QuantityKind_refined'][key].setdefault('Relation1',{}).update({'n'+str(idx):option['NondimensionalizesQuantityKind']})
                                            answers['QuantityKind_refined'][key].setdefault('Other1',{}).update({'n'+str(idx):Id + ' <|> ' + label})

                                elif r.get('SQUANTITY', {}).get('value') and r.get('SQLabel', {}).get('value') and r.get('SCLASS', {}).get('value'):

                                    for idx, (Id, label, Class) in enumerate(zip(r['SQUANTITY']['value'].split(' <|> '),r['SQLabel']['value'].split(' <|> '),r['SCLASS']['value'].split(' <|> '))):
                                        if Class.split('#')[1] == 'Quantity':
                                            answers['QuantityKind_refined'][key].setdefault('Relation2',{}).update({'s'+str(idx):option['SimilarToQuantity']})
                                            answers['QuantityKind_refined'][key].setdefault('Other2',{}).update({'s'+str(idx):Id + ' <|> ' + label})
                                        elif Class.split('#')[1] == 'QuantityKind':
                                            answers['QuantityKind_refined'][key].setdefault('Relation1',{}).update({'s'+str(idx):option['SimilarToQuantityKind']})
                                            answers['QuantityKind_refined'][key].setdefault('Other1',{}).update({'s'+str(idx):Id + ' <|> ' + label})

                # Research Field to Research Field Relations
                for key in answers['ResearchField']:
                    if answers['ResearchField'][key].get('MathModID') and answers['ResearchField'][key]['MathModID'] != 'not in MathModDB':
                        # If RF from MathModDB get Description
                        req=requests.get('https://sparql.ta4.m1.mardi.ovh/mathalgodb/query',
                                         params = {'format': 'json', 'query': query_rfs.format(answers['ResearchField'][key].get('MathModID'))},
                                         headers = {'User-Agent': 'MaRDMO_0.1 (https://zib.de; reidelbach@zib.de)'}).json()['results']['bindings']
                        for idx,r in enumerate(req):
                            answers['ResearchField'][key].update({'Description':r['quote']['value']})
                    for key2 in answers['ResearchField'][key].get('Relation1',{}):
                        Id,label = answers['ResearchField'][key]['Other1'][key2].split(' <|> ')[:2]
                        for idx, k in enumerate(answers['ResearchField']):
                            if label == answers['ResearchField'][k]['Name']:
                                answers['ResearchField'][key].setdefault('RelationRF1',{}).update({key2:[answers['ResearchField'][key]['Relation1'][key2],'RF'+str(idx+1)]})    
                        if not answers['ResearchField'][key].get('RelationRF1',{}).get(key2):
                            answers['ResearchField'][key].setdefault('RelationRF1',{}).update({key2:[answers['ResearchField'][key]['Relation1'][key2],Id]})
                 
                # Research Problem to Research Field Relations
                for key in answers['ResearchProblem']:
                    if answers['ResearchProblem'][key].get('MathModID') and answers['ResearchProblem'][key]['MathModID'] != 'not in MathModDB':
                        # If RP from MathModDB get Description
                        req=requests.get('https://sparql.ta4.m1.mardi.ovh/mathalgodb/query',
                                         params = {'format': 'json', 'query': query_rps.format(answers['ResearchProblem'][key].get('MathModID'))},
                                         headers = {'User-Agent': 'MaRDMO_0.1 (https://zib.de; reidelbach@zib.de)'}).json()['results']['bindings']
                        for idx,r in enumerate(req):
                            answers['ResearchProblem'][key].update({'Description':r['quote']['value']})
                    if answers['ResearchProblem'][key].get('ResearchField',{}).get(0):
                        Id,label = answers['ResearchProblem'][key]['ResearchField'][0].split(' <|> ')[:2]
                    elif len(answers['ResearchField'].keys()) == 1:
                        Id = answers['ResearchField'][0]['MathModID'] if answers['ResearchField'][0]['MathModID'] and answers['ResearchField'][0]['MathModID'] != 'not in MathModDB' else answers['ResearchField'][0]['ID'] if answers['ResearchField'][0]['ID'] else '' 
                        label = answers['ResearchField'][0]['Name']
                    else: 
                        # Stop if more than one Research Field present and no Field selected for Problem
                        return render(self.request,'MaRDMO/workflowError.html', {
                            'error': 'If more than one Research Field is defined the Research Problem(s) has/ve be assigned to them'
                            }, status=200)
                    for idx, key2 in enumerate(answers['ResearchField']):
                        if label == answers['ResearchField'][key2]['Name']:
                            answers['ResearchProblem'][key].setdefault('RelationRF1',{}).update({0:'RF'+str(idx+1)})
                
                # Research Problem to Research Problem Relations
                for key in answers['ResearchProblem']:
                    for key2 in answers['ResearchProblem'][key].get('Relation1',{}):
                        Id,label = answers['ResearchProblem'][key]['Other1'][key2].split(' <|> ')[:2]
                        for idx, k in enumerate(answers['ResearchProblem']):
                            if label == answers['ResearchProblem'][k]['Name']:
                                answers['ResearchProblem'][key].setdefault('RelationRP1',{}).update({key2:[answers['ResearchProblem'][key]['Relation1'][key2],'RP'+str(idx+1)]})
                        if not answers['ResearchProblem'][key].get('RelationRP1',{}).get(key2):
                            answers['ResearchProblem'][key].setdefault('RelationRP1',{}).update({key2:[answers['ResearchProblem'][key]['Relation1'][key2],Id]})
               
                # Add Research Problem to Model
                for idx,key in enumerate(answers['ResearchProblem']):
                    if answers['ResearchProblem'][key].get('MathModID') != 'not in MathModDB':
                        answers['Models'][0].setdefault('RelationRP1',{}).update({idx:'RP'+str(idx+1)})
                    elif answers['ResearchProblem'][key].get('Models') == option['Yes']:
                        answers['Models'][0].setdefault('RelationRP1',{}).update({idx:'RP'+str(idx+1)})

                # Convert Research Problems in additional Models
                for key in answers['AdditionalModel']:
                    if answers['AdditionalModel'][key].get('ResearchProblem'):
                        for key2 in answers['AdditionalModel'][key]['ResearchProblem']:
                            Id,label = answers['AdditionalModel'][key]['ResearchProblem'][key2].split(' <|> ')[:2]
                            for idx, k in enumerate(answers['ResearchProblem']):
                                if label == answers['ResearchProblem'][k]['Name']:
                                    answers['AdditionalModel'][key].setdefault('RelationRP1',{}).update({key2:'RP'+str(idx+1)})
                            if not answers['AdditionalModel'][key].get('RelationRP1',{}).get(key2):
                                answers['AdditionalModel'][key].setdefault('RelationRP1',{}).update({key2:Id})
                    else:
                        req=requests.get('https://sparql.ta4.m1.mardi.ovh/mathalgodb/query',
                                         params = {'format': 'json', 'query': query_models.format(answers['AdditionalModel'][key].get('MathModID'))},
                                         headers = {'User-Agent': 'MaRDMO_0.1 (https://zib.de; reidelbach@zib.de)'}).json()['results']['bindings']
                        for idx,r in enumerate(req):
                            answers['AdditionalModel'][key].setdefault('RelationRP1',{}).update({idx:r['answer']['value']})
                
                # Combine Model and additional Models
                if answers.get('AdditionalModel'):
                    answers['Models'][max(answers['AdditionalModel'].keys())+1] = answers['Models'].pop(list(answers['Models'].keys())[0])
                    answers.update({'AllModels':answers['Models']|answers['AdditionalModel']})
                else:
                    answers.update({'AllModels':answers['Models']})

                # Add Mathematical Model to Mathematical Model Relations
                for key in answers['AllModels']:
                    for key2 in answers['AllModels'][key].get('Relation1',{}):
                        Id,label = answers['AllModels'][key]['Other1'][key2].split(' <|> ')[:2]
                        for idx, k in enumerate(answers['AllModels']):
                            if label == answers['AllModels'][k]['Name']:
                                answers['AllModels'][key].setdefault('RelationMM1',{}).update({key2:[answers['AllModels'][key]['Relation1'][key2],'MM'+str(idx+1)]})
                        if not answers['AllModels'][key].get('RelationMM1',{}).get(key2):
                            answers['AllModels'][key].setdefault('RelationMM1',{}).update({key2:[answers['AllModels'][key]['Relation1'][key2],Id]})

                # Add Mathematical Formulation to Mathematical Formulation Relations 1
                for key in answers['MathematicalFormulation']:
                    for key2 in answers['MathematicalFormulation'][key].get('Relation2',{}):
                        Id,label = answers['MathematicalFormulation'][key]['Other2'][key2].split(' <|> ')[:2]
                        for idx, k in enumerate(answers['MathematicalFormulation']):
                            if label == answers['MathematicalFormulation'][k]['Name']:
                                answers['MathematicalFormulation'][key].setdefault('RelationMF1',{}).update({key2:[answers['MathematicalFormulation'][key]['Relation2'][key2],'MF'+str(idx+1)]})
                        if not answers['MathematicalFormulation'][key].get('RelationMF1',{}).get(key2):
                            answers['MathematicalFormulation'][key].setdefault('RelationMF1',{}).update({key2:[answers['MathematicalFormulation'][key]['Relation2'][key2],Id]})

                # Add Mathematical Formulation to Mathematical Formulation Relations 2
                for key in answers['MathematicalFormulation']:
                    for key2 in answers['MathematicalFormulation'][key].get('Relation3',{}):
                        Id,label = answers['MathematicalFormulation'][key]['Other3'][key2].split(' <|> ')[:2]
                        for idx, k in enumerate(answers['MathematicalFormulation']):
                            if label == answers['MathematicalFormulation'][k]['Name']:
                                answers['MathematicalFormulation'][key].setdefault('RelationMF2',{}).update({key2:[answers['MathematicalFormulation'][key]['Relation3'][key2],'MF'+str(idx+1)]})
                        if not answers['MathematicalFormulation'][key].get('RelationMF2',{}).get(key2):
                            answers['MathematicalFormulation'][key].setdefault('RelationMF2',{}).update({key2:[answers['MathematicalFormulation'][key]['Relation3'][key2],Id]})
                 
                # Add Mathematical Model to Mathematical Formulation Relations 1
                for key in answers['MathematicalFormulation']:
                    for key2 in answers['MathematicalFormulation'][key].get('Relation1',{}):
                        Id,label = answers['MathematicalFormulation'][key]['Other1'][key2].split(' <|> ')[:2]
                        for idx, k in enumerate(answers['AllModels']):
                            if label == answers['AllModels'][k]['Name']:
                                answers['MathematicalFormulation'][key].setdefault('RelationMM1',{}).update({key2:[answers['MathematicalFormulation'][key]['Relation1'][key2],idx+1,'MM'+str(idx+1)]})
                        if not answers['MathematicalFormulation'][key].get('RelationMM1',{}).get(key2):
                            answers['MathematicalFormulation'][key].setdefault('RelationMM1',{}).update({key2:[answers['MathematicalFormulation'][key]['Relation1'][key2],Id,Id]})

                # Add Task to Mathematical Formulation Relations 1
                for key in answers['MathematicalFormulation']:
                    for key2 in answers['MathematicalFormulation'][key].get('Relation4',{}):
                        Id,label = answers['MathematicalFormulation'][key]['Other4'][key2].split(' <|> ')[:2]
                        for idx, k in enumerate(answers['Task']):
                            if label == answers['Task'][k]['Name']:
                                answers['MathematicalFormulation'][key].setdefault('RelationT1',{}).update({key2:[answers['MathematicalFormulation'][key]['Relation4'][key2],idx+1,'T'+str(idx+1)]})
                        if not answers['MathematicalFormulation'][key].get('RelationT1',{}).get(key2):
                            answers['MathematicalFormulation'][key].setdefault('RelationT1',{}).update({key2:[answers['MathematicalFormulation'][key]['Relation4'][key2],Id,Id]})
                
                # Sort user defined Quantities / Quantitiy Kinds in respective Dictionaries
                for key in answers['Quantity']:
                    if key != 'MathModID':
                        if answers['Quantity'][key]['QorQK'] == option['Quantity']:
                            
                            if answers.get('Quantity_refined', {}).keys():
                                idx = max(answers['Quantity_refined'].keys())+1
                            else:
                                idx = 0
                            
                            answers.setdefault('Quantity_refined',{}).update({idx:{'QName':answers['Quantity'][key].get('Name',''),
                                                                                   'QDescription':answers['Quantity'][key].get('Description',''),
                                                                                   'ID':answers['Quantity'][key].get('ID') if answers['Quantity'][key].get('ID') else answers['Quantity'][key].get('Reference') if answers['Quantity'][key].get('Reference') else '',
                                                                                   'QProperties':answers['Quantity'][key].get('PropertiesQ'),
                                                                                   'Relation1':answers['Quantity'][key].get('RelationQ1',{}),
                                                                                   'Other1':answers['Quantity'][key].get('OtherQ1',{}),
                                                                                   'Relation2':answers['Quantity'][key].get('RelationQ2',{}),
                                                                                   'Other2':answers['Quantity'][key].get('OtherQ2',{}),
                                                                                   'QKName':answers['Quantity'][key].get('OtherQ2',{}).get(0,'').split(' <|> ')[-1],
                                                                                   'QKID':answers['Quantity'][key].get('OtherQ2',{}).get(0,'').split(' <|> ')[0]}})

                        elif answers['Quantity'][key]['QorQK'] == option['QuantityKind']:
                            
                            if answers.get('QuantityKind_refined', {}).keys():
                                idx = max(answers['QuantityKind_refined'].keys())+1
                            else:
                                idx = 0

                            answers.setdefault('QuantityKind_refined',{}).update({idx:{'QKName':answers['Quantity'][key].get('Name',''),
                                                                                       'QKDescription':answers['Quantity'][key].get('Description',''),
                                                                                       'ID':answers['Quantity'][key].get('ID',''),
                                                                                       'QKProperties':answers['Quantity'][key].get('PropertiesQK'),
                                                                                       'Relation1':answers['Quantity'][key].get('RelationQK1',{}),
                                                                                       'Other1':answers['Quantity'][key].get('OtherQK1',{}),
                                                                                       'Relation2':answers['Quantity'][key].get('RelationQK2',{}),
                                                                                       'Other2':answers['Quantity'][key].get('OtherQK2',{})}})

                # Add Quantity to Quantity Relations
#                for key in answers.get('Quantity_refined', []):
#                    for key2 in answers['Quantity_refined'][key].get('Relation1',{}):
#                        Id,label = answers['Quantity_refined'][key]['Other1'][key2].split(' <|> ')[:2]
#                        for idx, k in enumerate(answers['Quantity_refined']):
#                            if label == answers['Quantity_refined'][k]['QName']:
#                                answers['Quantity_refined'][key].setdefault('RelationQQ1',{}).update({key2:[answers['Quantity_refined'][key]['Relation1'][key2],'Q'+str(idx+1)]})
#                        if not answers['Quantity_refined'][key].get('RelationQQ1',{}).get(key2):
#                            answers['Quantity_refined'][key].setdefault('RelationQQ1',{}).update({key2:[answers['Quantity_refined'][key]['Relation1'][key2],Id]})

                label_to_index = {answers['Quantity_refined'][k]['QName']: idx for idx, k in enumerate(answers.get('Quantity_refined',{}))}
                for key in answers.get('Quantity_refined', []):
                    for key2 in answers['Quantity_refined'][key].get('Relation1', {}):
                        Id, label = answers['Quantity_refined'][key]['Other1'][key2].split(' <|> ')[:2]
                        if label in label_to_index:
                            idx = label_to_index[label]
                            answers['Quantity_refined'][key].setdefault('RelationQQ', {}).update({key2: [answers['Quantity_refined'][key]['Relation1'][key2], 'Q' + str(idx + 1)]})
                        else:
                            answers['Quantity_refined'][key].setdefault('RelationQQ', {}).update({key2: [answers['Quantity_refined'][key]['Relation1'][key2], Id]})

                # Add QuantityKind to QuantityKind Relations
                for key in answers.get('QuantityKind_refined', []):
                    for key2 in answers['QuantityKind_refined'][key].get('Relation1',{}):
                        Id,label = answers['QuantityKind_refined'][key]['Other1'][key2].split(' <|> ')[:2]
                        for idx, k in enumerate(answers['QuantityKind_refined']):
                            if label == answers['QuantityKind_refined'][k]['QKName']:
                                answers['QuantityKind_refined'][key].setdefault('RelationQKQK',{}).update({key2:[answers['QuantityKind_refined'][key]['Relation1'][key2],'QK'+str(idx+1)]})
                        if not answers['QuantityKind_refined'][key].get('RelationQKQK',{}).get(key2):
                            answers['QuantityKind_refined'][key].setdefault('RelationQKQK',{}).update({key2:[answers['QuantityKind_refined'][key]['Relation1'][key2],Id]})

                # Add Quantity to QuantityKind Relations
                for key in answers.get('Quantity_refined', []):
                    for key2 in answers['Quantity_refined'][key].get('Relation2',{}):
                        Id,label = answers['Quantity_refined'][key]['Other2'][key2].split(' <|> ')[:2]
                        for idx, k in enumerate(answers.get('QuantityKind_refined',[])):
                            if label == answers['QuantityKind_refined'][k].get('QKName'):
                                answers['Quantity_refined'][key].setdefault('RelationQQK',{}).update({key2:[answers['Quantity_refined'][key]['Relation2'][key2],'QK'+str(idx+1)]})
                        if not answers['Quantity_refined'][key].get('RelationQQK',{}).get(key2):
                            answers['Quantity_refined'][key].setdefault('RelationQQK',{}).update({key2:[answers['Quantity_refined'][key]['Relation2'][key2],Id]})
                
                # Add QuantityKind to Quantity Relations
                for key in answers.get('QuantityKind_refined', []):
                    for key2 in answers['QuantityKind_refined'][key].get('Relation2',{}):
                        Id,label = answers['QuantityKind_refined'][key]['Other2'][key2].split(' <|> ')[:2]
                        for idx, k in enumerate(answers['Quantity_refined']):
                            if label == answers['Quantity_refined'][k]['QName']:
                                answers['QuantityKind_refined'][key].setdefault('RelationQKQ',{}).update({key2:[answers['QuantityKind_refined'][key]['Relation2'][key2],'Q'+str(idx+1)]})
                        if not answers['QuantityKind_refined'][key].get('RelationQKQ',{}).get(key2):
                            answers['QuantityKind_refined'][key].setdefault('RelationQKQ',{}).update({key2:[answers['QuantityKind_refined'][key]['Relation2'][key2],Id]})
                                           
                # Add Quantity to Elements
                for key in answers['MathematicalFormulation']:
                    for key2 in answers['MathematicalFormulation'][key].get('Element',{}):
                        
                        if len(answers['MathematicalFormulation'][key]['Element'][key2]['Quantity'].split(' <|> ')) == 1:
                            
                            for k in answers['Quantity_refined']:
                                if answers['MathematicalFormulation'][key]['Element'][key2]['Quantity'].lower() == answers['Quantity_refined'][k]['QName'].lower():
                                    answers['MathematicalFormulation'][key]['Element'][key2].update(
                                        {'Info': 
                                            {'Name':answers['Quantity_refined'][k].get('QName',''),
                                             'Description':answers['Quantity_refined'][k].get('QDescription',''),
                                             'QID':answers['Quantity_refined'][k].get('MathModID') if answers['Quantity_refined'][k].get('MathModID') else answers['Quantity_refined'][k].get('ID',''),
                                             'QKName':answers['Quantity_refined'][k].get('QKName',''),
                                             'QKID':answers['Quantity_refined'][k].get('QKID','')}
                                        })
                            
                            for k in answers['QuantityKind_refined']:
                                if answers['MathematicalFormulation'][key]['Element'][key2]['Quantity'].lower() == answers['QuantityKind_refined'][k].get('QKName','').lower():
                                    answers['MathematicalFormulation'][key]['Element'][key2].update(
                                        {'Info':
                                            {'Description':answers['QuantityKind_refined'][k].get('QKDescription',''),
                                             'QKID':answers['QuantityKind_refined'][k].get('MathModID') if answers['QuantityKind_refined'][k].get('MathModID') else answers['QuantityKind_refined'][k].get('QKID',''),
                                             'QKName':answers['QuantityKind_refined'][k].get('QKName','')}
                                        })

                        elif len(answers['MathematicalFormulation'][key]['Element'][key2]['Quantity'].split(' <|> ')) >= 2:
                            
                            Id,label_qqk = answers['MathematicalFormulation'][key]['Element'][key2]['Quantity'].split(' <|> ')[:2]
                            label,qqk = label_qqk.rsplit(' ',1)
                            
                            if qqk == '(Quantity)':
                                for k in answers['Quantity_refined']:
                                    if label.lower() == answers['Quantity_refined'][k]['QName'].lower():
                                        answers['MathematicalFormulation'][key]['Element'][key2].update(
                                            {'Info':
                                                {'Name':answers['Quantity_refined'][k].get('QName',''),
                                                 'Description':answers['Quantity_refined'][k].get('QDescription',''),
                                                 'QID':answers['Quantity_refined'][k].get('MathModID') if answers['Quantity_refined'][k].get('MathModID') else answers['Quantity_refined'][k].get('ID',''),
                                                 'QKName':answers['Quantity_refined'][k].get('QKName',''),
                                                 'QKID':answers['Quantity_refined'][k].get('QKID','')}
                                            })
                            
                            if qqk == '(QuantityKind)':
                                for k in answers['QuantityKind_refined']:
                                    if label.lower() == answers['QuantityKind_refined'][k]['QKName'].lower():
                                        answers['MathematicalFormulation'][key]['Element'][key2].update(
                                            {'Info':
                                                {'Description':answers['QuantityKind_refined'][k].get('QKDescription',''),
                                                 'QKID':answers['QuantityKind_refined'][k].get('MathModID') if answers['QuantityKind_refined'][k].get('MathModID') else answers['QuantityKind_refined'][k].get('QKID',''),
                                                 'QKName':answers['QuantityKind_refined'][k].get('QKName','')}
                                            })               

                # Add Definition to Quantities
                for key in answers.get('Quantity_refined',[]):
                    for key2 in answers['MathematicalFormulation']:
                        if answers['MathematicalFormulation'][key2].get('DefinedQuantity'):
                            Id,label = answers['MathematicalFormulation'][key2]['DefinedQuantity'].split(' <|> ')[:2]
                            if label == answers['Quantity_refined'][key]['QName']:
                                answers['Quantity_refined'][key].update({'MDef':answers['MathematicalFormulation'][key2]})

                # Add Mathematical Model to Task Relations
                for key in answers['Task']:
                    for key2 in answers['Task'][key]['Model']:
                        Id,label = answers['Task'][key]['Model'][key2].split(' <|> ')[:2]
                        for idx, k in enumerate(answers['AllModels']):
                            if label == answers['AllModels'][k]['Name']:
                                answers['Task'][key].setdefault('RelationMM',{}).update({key2:'MM'+str(idx+1)})
                        if not answers['Task'][key].get('RelationMM',{}).get(key2):
                            answers['Task'][key].setdefault('RelationMM',{}).update({key2:Id})

                # Add Research Problem to Task Relations
                for key in answers['Task']:
                    for key2 in answers['Task'][key]['ResearchProblem']:
                        Id,label = answers['Task'][key]['ResearchProblem'][key2].split(' <|> ')[:2]
                        for idx, k in enumerate(answers['ResearchProblem']):
                            if label == answers['ResearchProblem'][k]['Name']:
                                answers['Task'][key].setdefault('RelationRP',{}).update({key2:'RP'+str(idx+1)})
                        if not answers['Task'][key].get('RelationRP',{}).get(key2):
                            answers['Task'][key].setdefault('RelationRP',{}).update({key2:Id})

                # Add Quantity / Quantity Kind to Task Relations
                for key in answers['Task']:
                    for key2 in answers['Task'][key].get('Relation2',{}):
                        Id,label_qqk = answers['Task'][key]['Other2'][key2].split(' <|> ')[:2]
                        label,qqk = label_qqk.rsplit(' ',1)
                        if qqk == '(Quantity)':
                            for idx, k in enumerate(answers['Quantity_refined']):
                                if label == answers['Quantity_refined'][k]['QName']:
                                    answers['Task'][key].setdefault('RelationQQK',{}).update({key2:[answers['Task'][key]['Relation2'][key2],'Q'+str(idx+1)]})
                            if not answers['Task'][key].get('RelationQQK',{}).get(key2):
                                answers['Task'][key].setdefault('RelationQQK',{}).update({key2:[answers['Task'][key]['Relation2'][key2],Id]})
                        elif qqk == '(QuantityKind)':
                            for idx, k in enumerate(answers['QuantityKind_refined']):
                                if label == answers['QuantityKind_refined'][k]['QKName']:
                                    answers['Task'][key].setdefault('RelationQQK',{}).update({key2:[answers['Task'][key]['Relation2'][key2],'QK'+str(idx+1)]})
                            if not answers['Task'][key].get('RelationQQK',{}).get(key2):
                                answers['Task'][key].setdefault('RelationQQK',{}).update({key2:[answers['Task'][key]['Relation2'][key2],Id]})

                # Add Task to Task Relations
                for key in answers['Task']:
                    for key2 in answers['Task'][key].get('Relation3',{}):
                        Id,label = answers['Task'][key]['Other3'][key2].split(' <|> ')[:2]
                        for idx, k in enumerate(answers['Task']):
                            if label == answers['Task'][k]['Name']:
                                answers['Task'][key].setdefault('RelationT',{}).update({key2:[answers['Task'][key]['Relation3'][key2],'T'+str(idx+1)]})
                        if not answers['Task'][key].get('RelationT',{}).get(key2):
                            answers['Task'][key].setdefault('RelationT',{}).update({key2:[answers['Task'][key]['Relation3'][key2],Id]})
                 
                # Add Entities to Publication Relations
                for key in answers['PublicationModel']:
                    for key2 in answers['PublicationModel'][key].get('Relation1',{}):

                        if len(answers['PublicationModel'][key]['Other1'][key2].split(' <|> ')) == 1:
                            answers['PublicationModel'][key].setdefault('RelationP',{}).update({key2:[answers['PublicationModel'][key]['Relation1'][key2],answers['PublicationModel'][key]['Other1'][key2]]})
                        elif len(answers['PublicationModel'][key]['Other1'][key2].split(' <|> ')) > 1:
                            
                            if len(answers['PublicationModel'][key]['Other1'][key2].split(' <|> ')) == 2:
                                Id,label_kind = answers['PublicationModel'][key]['Other1'][key2].split(' <|> ')
                                label,kind = label_kind.rsplit(' (',1)
                            elif len(answers['PublicationModel'][key]['Other1'][key2].split(' <|> ')) == 3:
                                Id,label,quote_kind = answers['PublicationModel'][key]['Other1'][key2].split(' <|> ')
                                quote,kind = quote_kind.rsplit(' (',1)
                            
                            if kind[:-1] == 'Research Field':
                                for idx, k in enumerate(answers['ResearchField']):
                                    if label == answers['ResearchField'][k]['Name']:
                                        answers['PublicationModel'][key].setdefault('RelationP',{}).update({key2:[answers['PublicationModel'][key]['Relation1'][key2],'RF'+str(idx+1)]})
                                if not answers['PublicationModel'][key].get('RelationP',{}).get(key2):
                                    answers['PublicationModel'][key].setdefault('RelationP',{}).update({key2:[answers['PublicationModel'][key]['Relation1'][key2],Id]})
                            elif kind[:-1] == 'Research Problem':
                                for idx, k in enumerate(answers['ResearchProblem']):
                                    if label == answers['ResearchProblem'][k]['Name']:
                                        answers['PublicationModel'][key].setdefault('RelationP',{}).update({key2:[answers['PublicationModel'][key]['Relation1'][key2],'RP'+str(idx+1)]})
                                if not answers['PublicationModel'][key].get('RelationP',{}).get(key2):
                                    answers['PublicationModel'][key].setdefault('RelationP',{}).update({key2:[answers['PublicationModel'][key]['Relation1'][key2],Id]})

                            elif kind[:-1] == 'Mathematical Model':
                                for idx, k in enumerate(answers['AllModels']):
                                    if label == answers['AllModels'][k]['Name']:
                                        answers['PublicationModel'][key].setdefault('RelationP',{}).update({key2:[answers['PublicationModel'][key]['Relation1'][key2],'MM'+str(idx+1)]})
                                if not answers['PublicationModel'][key].get('RelationP',{}).get(key2):
                                    answers['PublicationModel'][key].setdefault('RelationP',{}).update({key2:[answers['PublicationModel'][key]['Relation1'][key2],Id]})

                            elif kind[:-1] == 'Quantity':
                                
                                if answers['PublicationModel'][key].get('RelationP'):
                                    key2 = max(answers['PublicationModel'][key]['RelationP'].keys()) + 1
                                else: 
                                    key2 = 0
                                
                                answers['PublicationModel'][key].setdefault('RelationP',{}).update({key2:[answers['PublicationModel'][key]['Relation1'][key2],label]})

                            elif kind[:-1] == 'Quantity Kind':
                                
                                if answers['PublicationModel'][key].get('RelationP'):
                                    key2 = max(answers['PublicationModel'][key]['RelationP'].keys()) + 1
                                else:
                                    key2 = 0
                                
                                answers['PublicationModel'][key].setdefault('RelationP',{}).update({key2:[answers['PublicationModel'][key]['Relation1'][key2],label]})
                            
                            elif kind[:-1] == 'Mathematical Formulation':
                                for idx, k in enumerate(answers['MathematicalFormulation']):
                                    if label == answers['MathematicalFormulation'][k]['Name']:
                                        answers['PublicationModel'][key].setdefault('RelationP',{}).update({key2:[answers['PublicationModel'][key]['Relation1'][key2],'MF'+str(idx+1)]})
                                if not answers['PublicationModel'][key].get('RelationP',{}).get(key2):
                                    answers['PublicationModel'][key].setdefault('RelationP',{}).update({key2:[answers['PublicationModel'][key]['Relation1'][key2],Id]})

                            elif kind[:-1] == 'Task':
                                for idx, k in enumerate(answers['Task']):
                                    if label == answers['Task'][k]['Name']:
                                        answers['PublicationModel'][key].setdefault('RelationP',{}).update({key2:[answers['PublicationModel'][key]['Relation1'][key2],'T'+str(idx+1)]})
                                if not answers['PublicationModel'][key].get('RelationP',{}).get(key2):
                                    answers['PublicationModel'][key].setdefault('RelationP',{}).update({key2:[answers['PublicationModel'][key]['Relation1'][key2],Id]})             
                 
                # Load MaRDI Markdown Workflow Template
                path = os.path.join(os.path.dirname(__file__), 'templates', 'MaRDMO', 'modelTemplate.md')
                with open(path, 'r') as file:
                    markdown_template = file.read()

                # Create a Django Template object
                template = Template(markdown_template)

                # Render the template with the data
                context = Context({'title':self.project.title}|answers|option)
                markdown_workflow = template.render(context)

                # Provide Documentation as Markdown Download
                response = HttpResponse(os.linesep.join([s.strip() for s in markdown_workflow.splitlines() if s.strip()]), content_type="application/md")
                response['Content-Disposition'] = 'filename="model.md"'

                return response


                return render(self.request,'MaRDMO/workflowError.html', {
                    'error': 'The documentation of Mathematical Models will soon be integrated!'
                    }, status=200)
            else:
                # Stop if no Documentation Type chosen
                return render(self.request,'MaRDMO/workflowError.html', {
                    'error': 'Missing Documentation Type!'
                    }, status=200)


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
        elif answers['Settings']['Documentation'] == option['Search']:
            
### SPARQL via Research Objectives ################################################################################################################################################################
            
            # SPARQL string definitions
            quote_str = ''
            res_obj_strs = ''

            # If SPARQL query via research objective desired
            if answers['Search']['Search Objective'] == option['Yes']:
                quote_str = quote_sparql
                # Separate key words for SPARQL query vie research objective
                if answers['Search'].get('Objective Keywords'):
                    for res_obj in answers['Search']['Objective Keywords'].values():
                        # Define Filters for SPARQL queries
                        res_obj_strs+=res_obj_sparql.format(res_obj.lower())

### SPARQL via Research Disciplines ###############################################################################################################################################################

            # SPARQL string definitions
            res_disc_str = ''

            # If SPARQL query via research discipline desired
            if answers['Search']['Search Discipline'] == option['Yes']:
                # Separate disciplines for SPARQL query via research discipline 
                if answers['Search'].get('Discipline Keywords'):
                    for res_disc in answers['Search']['Discipline Keywords'].values():
                        # Define Filters for SPARQL queries
                        res_disc_str += res_disc_sparql.format(P5, res_disc.split('<|>')[0].split(':')[1])

### SPARQL via Mathematical Models, Methods, Softwares, Input or Output Data Sets #################################################################################################################

            # SPARQL string definitions
            mmsios_str = ''

            # If SPARQL query via Mathematical Models, Methods, Softwares, Input or Output Data Sets
            if answers['Search']['Search Entities'] == option['Yes']:
                # Separate Mathematical Model, Methods, Software, Input or Output Data Sets
                if answers['Search'].get('Entities Keywords'):
                    for mmsio in answers['Search']['Entities Keywords'].values():
                        # Define Filters for SPARQL queries
                        mmsios_str += mmsio_sparql.format(P6, mmsio.split('<|>')[0].split(':')[1])

### Set up Query, query MaRDI Portal and return Results ###########################################################################################################################################

            # Set up entire SPARQL query
            query = query_base.format(P4,Q2,res_disc_str,mmsios_str,quote_str,res_obj_strs)

            # Query MaRDI Portal
            results = self.get_results(mardi_endpoint, query)

            # Number of Results
            no_results = str(len(results))
            
            # Generate Links to Wikipage and Knowledge Graoh Entry of Results
            links=[]
            for result in results:
                links.append([result["label"]["value"],mardi_wiki+result["label"]["value"].replace(' ','_'),mardi_wiki+'Item:'+result["qid"]["value"]])

            return render(self.request,'MaRDMO/workflowSearch.html', {
                    'noResults': no_results,
                    'links': links
                    }, status=200)
        
        else:
            # Stop if Workflow Documentation or Search not chosen
            return render(self.request,'MaRDMO/workflowError.html', {
                    'error': 'Missing Operation Modus!'
                    }, status=200)
       
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
                elif fact[0] == Quantity:
                    if len(fact) == 3:
                        data.append(fact[0](fact[1],prop_nr=fact[2]))
                    elif len(fact) == 4:
                        data.append(fact[0](fact[1],prop_nr=fact[2],qualifiers=fact[3]))
                else:
                    if len(fact) == 3:
                        data.append(fact[0](value=fact[1],prop_nr=fact[2]))
                    elif len(fact) == 4:
                        data.append(fact[0](value=fact[1],prop_nr=fact[2],qualifiers=fact[3]))
        item.claims.add(data)
            
        item.write()

        return item.id

    def get_results(self,endpoint_url, query):
        '''Perform SPARQL Queries via Get requests'''
        req=requests.get(endpoint_url, params = {'format': 'json', 'query': query}, headers = {'User-Agent': 'MaRDMO_0.1 (https://zib.de; reidelbach@zib.de)'}).json()
        return req["results"]["bindings"]
    
    def portal_wikidata_check(self,answers,public,preview):
        '''Function checks if an entry is on MaRDI portal and returns its QID
           or on Wikidata and copies the entry to the MaRDI portal and returns
           its QID.'''
        # Store Label and Description
        entry = [answers.get('Name'), answers.get('Description')]
        if answers['ID']:
            # IF ID exists, split in prefix and qnumber
            prefix, qnumber = answers['ID'].split(':')
            if prefix == 'mardi':
                # Store MaRDI QID
                qid = qnumber
            elif prefix == 'wikidata':
                # IF Wikidata QID, check Publication Type
                if public == option['Public'] and preview == option['No']:
                    #Create Entry on MaRDI Portal and store MaRDI QID
                    qid = self.entry(entry[0], entry[1] , [(ExternalID, qnumber, P2)])
                else:
                    qid = 'tbd'
            else:
                qid = None
        else:
            qid = answers['ID']

        return qid, entry

    def Entry_Generator_Paper_Supplements(self, props, relations, add_relations):
        '''This function takes a paper supplement (i.e. authors, languages, journal) and creates the corresponding wikibase entries.'''
        qids = []
        for prop in props.values():
            if prop and prop != 'NONE':
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

    def refine(self,answers):
        '''This function takes user answers and performs SPARQL queries to MaRDI portal.'''
        
        entities = ['NonMathematicalDiscipline','Models','Software','DataSet','Method','Hardware','ExperimentalDevice','ResearchField',
                    'ResearchProblem','AdditionalModel','MathematicalFormulation','Quantity','Task','PublicationModel']

        for entity in entities:
            for key in answers[entity]:
                # Refining IDs, Names and Descriptions of entities
                if answers[entity][key].get('ID') and answers[entity][key].get('ID') != 'not in MathModDB':
                    if type(answers[entity][key]['ID']) == str:
                        ID, Name, Description = answers[entity][key]['ID'].split(' <|> ')
                        if re.match(r"mardi:Q[0-9]+", ID): 
                            answers[entity][key].update({'ID':ID, 'Name':Name, 'Description':Description})
                        else:
                            mardiID = self.find_item(Name,Description)
                            if mardiID:
                                answers[entity][key].update({'ID':f"mardi:{mardiID}", 'Name':Name, 'Description':Description})
                            else:
                                answers[entity][key].update({'ID':ID, 'Name':Name, 'Description':Description})
                    else:
                        for ikey in answers[entity][key]['ID']:
                            ID, Name, Description = answers[entity][key]['ID'][ikey].split(' <|> ')
                            if re.match(r"mardi:Q[0-9]+", ID):
                                answers[entity][key]['ID'].update({ikey:{'ID':ID, 'Name':Name, 'Description':Description}})
                            else:
                                mardiID = self.find_item(Name,Description)
                                if mardiID:
                                    answers[entity][key]['ID'].update({ikey:{'ID':f"mardi:{mardiID}", 'Name':Name, 'Description':Description}})
                                else:
                                    answers[entity][key]['ID'].update({ikey:{'ID':ID, 'Name':Name, 'Description':Description}})
                else:
                    if answers[entity][key].get('Name') and answers[entity][key].get('Description'):
                        mardiID = self.find_item(answers[entity][key]['Name'],answers[entity][key]['Description'])
                        if mardiID:
                            answers[entity][key].update({'ID':f"mardi:{mardiID}"})
                        else:
                            answers[entity][key].update({'ID':None})
                    else:
                        answers[entity][key].update({'ID':None})
                # Refining Subproperties of entities
                if answers[entity][key].get('SubProperty'):
                    for ikey in answers[entity][key]['SubProperty']:
                        ID, Name, Description = answers[entity][key]['SubProperty'][ikey].split(' <|> ')
                        if re.match(r"mardi:Q[0-9]+", ID):
                            answers[entity][key]['SubProperty'].update({ikey:{'ID':ID, 'Name':Name, 'Description':Description}})
                        else:
                            mardiID = self.find_item(Name,Description)
                            if mardiID:
                                answers[entity][key]['SubProperty'].update({ikey:{'ID':f"mardi:{mardiID}", 'Name':Name, 'Description':Description}})
                            else:
                                answers[entity][key]['SubProperty'].update({ikey:{'ID':ID, 'Name':Name, 'Description':Description}})
                if answers[entity][key].get('SubProperty2'):
                    for ikey in answers[entity][key]['SubProperty2']:
                        ID, Name, Description = answers[entity][key]['SubProperty2'][ikey].split(' <|> ')
                        if re.match(r"mardi:Q[0-9]+", ID):
                            answers[entity][key]['SubProperty2'].update({ikey:{'ID':ID, 'Name':Name, 'Description':Description}})
                        else:
                            mardiID = self.find_item(Name,Description)
                            if mardiID:
                                answers[entity][key]['SubProperty2'].update({ikey:{'ID':f"mardi:{mardiID}", 'Name':Name, 'Description':Description}})
                            else:
                                answers[entity][key]['SubProperty2'].update({ikey:{'ID':ID, 'Name':Name, 'Description':Description}})
                if answers[entity][key].get('MathModID'):
                    if type(answers[entity][key]['MathModID']) == str:
                        if answers[entity][key]['MathModID'] != 'not in MathModDB':
                            ID, Name = answers[entity][key]['MathModID'].split(' <|> ')
                            answers[entity][key].update({'MathModID':ID,'Name':Name})
                    else:
                        for ikey in answers[entity][key]['MathModID']:
                            ID, Name = answers[entity][key]['MathModID'][ikey].split(' <|> ')
                            answers[entity].setdefault('MathModID',{}).update({ikey:{'MathModID':ID, 'Name':Name}})
        return answers

    def Entry_Generator(self,Type,Generate,Relations,answers):
        '''Function queries Wikidata/MaRDI KG, uses and generates entries in MaRDI Knowledge Graph.'''
        
        qids=[]
        for key in answers[Type].keys():
            # Check if on Portal or in Wikidata, integrate Wikidata entry if desired
            qid, entry = self.portal_wikidata_check(answers[Type][key], answers['Settings']['Public'], answers['Settings']['Preview'])        
            # Update User answers
            if qid: 
                qids.append(qid)
                answers[Type][key].update({'mardiId': qid, 'uri': f"{mardi_wiki}Item:{qid}"})
            
            if Generate[0]:
                # Stop if no label and quote is provided for entry to generate
                if not (qid or entry[0] and entry[1]):
                    return qids, answers, [0,key]
    
                # Get subproperty of 'new' entity
                subqids = []
                subqids2 = []
 
                if Generate[1]:
                    
                    # Define Qualifier for Entries
                    answers[Type][key].update({'Qualifiers':Qualifiers()})

                    if Type == 'ExperimentalDevice' and answers['Settings']['WorkflowType'] == option['Analysis']:

                        if answers['Settings']['Public'] == option['Public'] and answers['Settings']['Preview'] == option['No']:
                            # Add Version as qualifier of 'uses' statement
                            if answers[Type][key].get('Version'):
                                answers[Type][key]['Qualifiers'].add(String(prop_nr=Relations[3], value=answers[Type][key].get('Version')))
                            # Add Serial Number as qualifier of 'uses' statement
                            if answers[Type][key].get('SerialNumber'):
                                answers[Type][key]['Qualifiers'].add(String(prop_nr=Relations[4], value=answers[Type][key].get('SerialNumber')))
                        
                        # Search and add Location as qualifier of 'uses' statement 
                        for subkey in answers[Type][key].get('SubProperty', {}).keys():
                            if answers[Type][key]['SubProperty'][subkey]: 
                                location, _ = self.portal_wikidata_check(answers[Type][key]['SubProperty'][subkey], answers['Settings']['Public'], answers['Settings']['Preview'])
                                answers[Type][key]['SubProperty'][subkey].update({'mardiId': location, 'uri': f"{mardi_wiki}Item:{location}"})
                                if answers['Settings']['Public'] == option['Public'] and answers['Settings']['Preview'] == option['No']:
                                    answers[Type][key]['Qualifiers'].add(Item(prop_nr=Relations[1], value=location))
                        
                        # Search and add available Software as qualifier of 'uses' statement
                        for subkey in answers[Type][key].get('SubProperty2', {}).keys():
                            if answers[Type][key]['SubProperty2'][subkey]:
                                availSoftware, _ = self.portal_wikidata_check(answers[Type][key]['SubProperty2'][subkey], answers['Settings']['Public'], answers['Settings']['Preview'])
                                answers[Type][key]['SubProperty2'][subkey].update({'mardiId': availSoftware, 'uri': f"{mardi_wiki}Item:{availSoftware}"})
                                if answers['Settings']['Public'] == option['Public'] and answers['Settings']['Preview'] == option['No']:
                                    answers[Type][key]['Qualifiers'].add(Item(prop_nr=Relations[2], value=availSoftware))
                    
                    elif Type == 'Hardware' and answers['Settings']['WorkflowType'] == option['Computation']:
                        
                        # Search and add CPU, with number of cores and ID (wikidata / wikichip)
                        cpuIDs=[]
                        for subkey in answers[Type][key].get('SubProperty', {}).keys():
                            cpuID = self.find_item(answers[Type][key]['SubProperty'][subkey]['Name'],answers[Type][key]['SubProperty'][subkey]['Description'])
                            if not cpuID:
                                if answers['Settings']['Public'] == option['Public'] and answers['Settings']['Preview'] == option['No']:
                                    cpuID = self.entry(
                                                answers[Type][key]['SubProperty'][subkey]['Name'],answers[Type][key]['SubProperty'][subkey]['Description'],
                                                [(Item,Relations[0],Relations[3]),(Quantity,answers['Hardware'][key].get('Core') if answers['Hardware'][key].get('Core') else '1',Relations[4])]+
                                                [(ExternalID,answers[Type][key]['SubProperty'][subkey]['ID'].split(':')[-1],Relations[5] if 'wikidata' in answers[Type][key]['SubProperty'][subkey]['ID'] else Relations[6])]
                                                )
                                else:
                                    cpuID = 'tbd'
                            answers[Type][key]['SubProperty'][subkey].update({'mardiId': cpuID, 'uri': f"{mardi_wiki}Item:{cpuID}"})
                            cpuIDs.append(cpuID)

                        # Search and add Compilers as qualifiers of 'uses' statement
                        for subkey in answers[Type][key].get('SubProperty2', {}).keys():
                            if answers[Type][key]['SubProperty2'][subkey]:
                                compiler, _ = self.portal_wikidata_check(answers[Type][key]['SubProperty2'][subkey], answers['Settings']['Public'], answers['Settings']['Preview'])
                                answers[Type][key]['SubProperty2'][subkey].update({'mardiId': compiler, 'uri': f"{mardi_wiki}Item:{compiler}"})
                                if answers['Settings']['Public'] == option['Public'] and answers['Settings']['Preview'] == option['No']:
                                    answers[Type][key]['Qualifiers'].add(Item(prop_nr=Relations[2], value=compiler))

                    else:
                        for subkey in answers[Type][key].get('SubProperty', {}).keys():
                            # Check if subproperty on Portal or in Wikidata (store QID and string)
                            if answers[Type][key]['SubProperty'][subkey]: 
                                subqid, subentry = self.portal_wikidata_check(answers[Type][key]['SubProperty'][subkey], answers['Settings']['Public'], answers['Settings']['Preview'])
                                answers[Type][key]['SubProperty'][subkey].update({'mardiId': subqid, 'uri': f"{mardi_wiki}Item:{subqid}"})
                                subqids.append(subqid)
                                if answers['Settings']['Public'] == option['Public'] and answers['Settings']['Preview'] == option['No']:
                                    answers[Type][key]['Qualifiers'].add(Item(prop_nr=Relations[1], value=subqid))

                        for subkey in answers[Type][key].get('SubProperty2', {}).keys():
                            # Check if subproperty2 on Portal or in Wikidata (store QID and string)
                            if answers[Type][key]['SubProperty2'][subkey]:
                                    subqid2, subentry = self.portal_wikidata_check(answers[Type][key]['SubProperty2'][subkey], answers['Settings']['Public'], answers['Settings']['Preview'])
                                    answers[Type][key]['SubProperty2'][subkey].update({'mardiId': subqid2, 'uri': f"{mardi_wiki}Item:{subqid2}"})
                                    subqids2.append(subqid2)

                        # Stop if entry has no QID and its subproperty has no QID    
                        if not (qid or subqids):
                            return qids, answers, [1,key]
    
                # Generate Entry QID
                if not qid:
                    # If desired generate Entry in MaRDI KG and update User answers
                    if answers['Settings']['Public'] == option['Public'] and answers['Settings']['Preview'] == option['No']:
                        if Type == 'Hardware':
                            qids.append(self.entry(
                                entry[0],entry[1],
                                [(Item,Relations[0],Relations[3])] +
                                [(Item,cpuID,Relations[1],Qualifiers().add(Quantity(answers['Hardware'][key].get('Node') if answers['Hardware'][key].get('Node') else '1',prop_nr=Relations[7]))) for cpuID in cpuIDs]))
                        elif Type == 'ExperimentalDevice':
                            qids.append(self.entry(
                                entry[0],entry[1],
                                [(Item,Relations[0],P4)]))
                        else:
                            qids.append(self.entry(entry[0],entry[1], 
                                                   [(Item,Relations[0],P4)]+
                                                   [(ExternalID,answers[Type][key].get('MathModID','') if answers[Type][key].get('MathModID','') != 'not in MathModDB' else '',P24)]+
                                                   [(Item,subqid,Relations[1]) for subqid in subqids]+
                                                   [(Item,subqid2,Relations[2]) for subqid2 in subqids2]+ 
                                                   [(String,re.sub("\$","",form.lstrip()),P18) for form in answers[Type][key].get('Formular',{}).values()]+
                                                   [(ExternalID,answers[Type][key].get('Reference','').split(':')[-1],
                                                     P16 if answers[Type][key].get('Reference','').split(':')[0] == 'doi' else P20 if answers[Type][key].get('Reference','').split(':')[-1] == 'swmath' else P24 if answers[Type][key].get('Reference','').split(':')[-1] == 'url' else '')]))
                        answers[Type][key].update({'mardiId': qids[-1], 'uri': f"{mardi_wiki}Item:{qids[-1]}"})
                    else:
                        answers[Type][key].update({'mardiId': 'tbd', 'uri': f"{mardi_wiki}Item:{qid}"})
            else:
                if not qid:
                    return qids, answers, [2,key]

        return qids, answers, [-1,-1]
            
    def find_item(self, label, description, api=mardi_api, language="en"):
        # Perform label-based search
        response = requests.get(api, params={
            'action': 'wbsearchentities',
            'format': 'json',
            'language': 'en',
            'type': 'item',
            'limit': 10,
            'search': label
        }, headers={'User-Agent': 'MaRDMO_0.1 (https://zib.de; reidelbach@zib.de)'})
        data = response.json()
        # Filter results based on description
        matched_items = [item for item in data['search'] if item.get('description') == description] 
        if matched_items:
            # Return the ID of the first matching item
            return matched_items[0]['id']
        else:
            # No matching item found
            return None

    def get_answer(self, val, uName, dName, Id, set_prefix=False, set_index=False, collection_index=False, option_text=False, external_id=False):
        '''Function that retrieves individual User answers'''
        val.setdefault(uName, {})
        try:
            values = self.project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri=Id))
        except:
            values = []
        for value in values:
            if value.option:
                if option_text:
                    if set_prefix:
                        if set_index:
                            if collection_index:
                                if external_id:
                                    val[uName].setdefault(int(value.set_prefix), {}).setdefault(value.set_index, {}).setdefault(dName, {}).update({value.collection_index:[value.option_uri, value.external_id]})
                                else:
                                    val[uName].setdefault(int(value.set_prefix), {}).setdefault(value.set_index, {}).setdefault(dName, {}).update({value.collection_index:[value.option_uri, value.text]})
                            else:
                                if external_id:
                                    val[uName].setdefault(int(value.set_prefix), {}).setdefault(value.set_index, {}).update({dName:[value.option_uri, value.external_id]})
                                else:
                                    val[uName].setdefault(int(value.set_prefix), {}).setdefault(value.set_index, {}).update({dName:[value.option_uri, value.text]})
                        else:
                            if collection_index:
                                if external_id:
                                    val[uName].setdefault(int(value.set_prefix), {}).setdefault(dName, {}).update({value.collection_index:[value.option_uri, value.external_id]})
                                else:
                                    val[uName].setdefault(int(value.set_prefix), {}).setdefault(dName, {}).update({value.collection_index:[value.option_uri, value.text]})
                            else:
                                if external_id:
                                    val[uName].setdefault(int(value.set_prefix), {}).update({dName:[value.option_uri, value.external_id]})
                                else:
                                    val[uName].setdefault(int(value.set_prefix), {}).update({dName:[value.option_uri, value.text]})
                    else:
                        if set_index:
                            if collection_index:
                                if external_id:
                                    val[uName].setdefault(value.set_index, {}).setdefault(dName, {}).update({value.collection_index:[value.option_uri, value.external_id]})
                                else:
                                    val[uName].setdefault(value.set_index, {}).setdefault(dName, {}).update({value.collection_index:[value.option_uri, value.text]})
                            else:
                                if external_id:
                                    val[uName].setdefault(value.set_index, {}).update({dName:[value.option_uri, value.external_id]})
                                else:
                                    val[uName].setdefault(value.set_index, {}).update({dName:[value.option_uri, value.text]})
                        else:
                            if collection_index:
                                if external_id:
                                    val[uName].setdefault(dName, {}).update({value.collection_index:[value.option_uri, value.external_id]})
                                else:
                                    val[uName].setdefault(dName, {}).update({value.collection_index:[value.option_uri, value.text]})
                            else:
                                if external_id:
                                    val[uName].update({dName:[value.option_uri, value.external_id]})
                                else:
                                    val[uName].update({dName:[value.option_uri, value.text]})
                else:
                    if set_prefix:
                        if set_index:
                            if collection_index:
                                if len(value.set_prefix.split('|')) == 1:
                                    val[uName].setdefault(int(value.set_prefix), {}).setdefault(value.set_index, {}).setdefault(dName, {}).update({value.collection_index:value.option_uri})
                                elif len(value.set_prefix.split('|')) == 2:
                                    prefix = value.set_prefix.split('|')
                                    val[uName].setdefault(int(prefix[0]), {}).setdefault(value.set_index, {}).setdefault(dName, {}).update({value.collection_index:value.option_uri})
                            else:
                                if len(value.set_prefix.split('|')) == 1:
                                    val[uName].setdefault(int(value.set_prefix), {}).setdefault(dName, {}).update({value.set_index:value.option_uri})
                                elif len(value.set_prefix.split('|')) == 2:
                                    prefix = value.set_prefix.split('|')
                                    val[uName].setdefault(int(prefix[0]), {}).setdefault(dName, {}).update({value.set_index:value.option_uri})
                        else:
                            if collection_index:
                                val[uName].setdefault(int(value.set_prefix), {}).setdefault(dName, {}).update({value.collection_index:value.option_uri})
                            else:
                                val[uName].setdefault(int(value.set_prefix), {}).update({dName:value.option_uri})
                    else:
                        if set_index:
                            if collection_index:
                                val[uName].setdefault(value.set_index, {}).setdefault(dName, {}).update({value.collection_index:value.option_uri})
                            else:
                                val[uName].setdefault(value.set_index, {}).update({dName:value.option_uri})
                        else:
                            if collection_index:
                                val[uName].setdefault(dName, {}).update({value.collection_index:value.option_uri})
                            else:
                                val[uName].update({dName:value.option_uri})
            elif value.text and value.text != 'NONE':
                if set_prefix:
                    if set_index:
                        if collection_index:
                            if external_id:
                                val[uName].setdefault(int(value.set_prefix), {}).setdefault(value.set_index, {}).setdefault(dName, {}).update({value.collection_index:value.external_id})
                            else:
                                val[uName].setdefault(int(value.set_prefix), {}).setdefault(value.set_index, {}).setdefault(dName, {}).update({value.collection_index:value.text})
                        else:
                            if external_id:
                                if len(value.set_prefix.split('|')) == 1:
                                    val[uName].setdefault(int(value.set_prefix), {}).setdefault(dName, {}).update({value.set_index:value.external_id})
                                elif len(value.set_prefix.split('|')) == 2:
                                    prefix = value.set_prefix.split('|')
                                    if 'Element' in dName:
                                        val[uName].setdefault(int(prefix[0]), {}).setdefault(dName.split(' ')[0], {}).setdefault(value.set_index, {}).update({dName.split(' ')[1]:value.external_id})
                                    else: 
                                        val[uName].setdefault(int(prefix[0]), {}).setdefault(dName, {}).update({value.set_index:value.external_id})
                            else:
                                if len(value.set_prefix.split('|')) == 1: 
                                    val[uName].setdefault(int(value.set_prefix), {}).setdefault(dName, {}).update({value.set_index:value.text})
                                elif len(value.set_prefix.split('|')) == 2:
                                    prefix = value.set_prefix.split('|')
                                    val[uName].setdefault(int(prefix[0]), {}).setdefault(dName.split(' ')[0], {}).setdefault(value.set_index, {}).update({dName.split(' ')[1]:value.text})
                    else:
                        if collection_index:
                            if external_id:
                                val[uName].setdefault(int(value.set_prefix), {}).setdefault(dName, {}).update({value.collection_index:value.external_id})
                            else:
                                val[uName].setdefault(int(value.set_prefix), {}).setdefault(dName, {}).update({value.collection_index:value.text})
                        else:
                            if external_id:
                                val[uName].setdefault(int(value.set_prefix), {}).update({dName:value.external_id})
                            else:
                                val[uName].setdefault(int(value.set_prefix), {}).update({dName:value.text})
                else:
                    if set_index:
                        if collection_index:
                            if external_id:
                                val[uName].setdefault(value.set_index, {}).setdefault(dName, {}).update({value.collection_index:value.external_id})
                            else:
                                val[uName].setdefault(value.set_index, {}).setdefault(dName, {}).update({value.collection_index:value.text})
                        else:
                            if external_id:
                                val[uName].setdefault(value.set_index, {}).update({dName:value.external_id})
                            else:
                                val[uName].setdefault(value.set_index, {}).update({dName:value.text})
                    else:
                        if collection_index:
                            if external_id:
                                val[uName].setdefault(dName, {}).update({value.collection_index:value.external_id})
                            else:
                                val[uName].setdefault(dName, {}).update({value.collection_index:value.text})
                        else:
                            if external_id:
                                val[uName].update({dName:value.external_id})
                            else:
                                val[uName].update({dName:value.text})
            elif value.set_index:
                if set_prefix:
                    if set_index:
                        if collection_index:
                            val[uName].setdefault(int(value.set_prefix), {}).setdefault(value.set_index, {}).setdefault(dName, {}).update({value.collection_index:None})
                        else:
                            val[uName].setdefault(int(value.set_prefix), {}).setdefault(value.set_index, {}).update({dName:None})
                    else:
                        if collection_index:
                            val[uName].setdefault(int(value.set_prefix), {}).setdefault(dName, {}).update({value.collection_index:None})
                        else:
                            val[uName].setdefault(int(value.set_prefix), {}).update({dName:None})
                else:
                    if set_index:
                        if collection_index:
                            val[uName].setdefault(value.set_index, {}).setdefault(dName, {}).update({value.collection_index:None})
                        else:
                            val[uName].setdefault(value.set_index, {}).update({dName:None})
                    else:
                        if collection_index:
                            val[uName].setdefault(dName, {}).update({value.collection_index:None})
                        else:
                            val[uName].update({dName:None})
        return val

