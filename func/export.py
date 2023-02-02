from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.conf import settings
from rdmo.projects.exports import Export
from rdmo.questions.models import Question
from rdmo.core.utils import render_to_csv
from django.shortcuts import render

from .para import *
import requests

from owlready2 import *
import nltk
import numpy as np
import sklearn as sk
import pypandoc

class MaRDIExport(Export):

    def render(self):
        '''Function that renders User answers to MaRDI template
           (adjusted from csv export)'''
       
        # Check if MaRDI Questionaire is used
        if str(self.project.catalog) != 'MaRDI':
            return render(self.request,'error1.html')

        # Get Data - Questions and User Answers
        queryset = self.project.values.filter(snapshot=None)
        data = []
        for question in Question.objects.order_by_catalog(self.project.catalog):
            if question.questionset.is_collection and question.questionset.attribute:
                if question.questionset.attribute.uri.endswith('/id'):
                    set_attribute_uri = question.questionset.attribute
                else:
                    set_attribute_uri = question.questionset.attribute.uri.rstrip('/') + '/id'
                for value_set in queryset.filter(attribute__uri=question.questionset.attribute.uri):
                    values = queryset.filter(attribute=question.attribute, set_index=value_set.set_index) \
                                     .order_by('set_prefix', 'set_index', 'collection_index')
                    data.append([question.attribute.uri+'_'+self.stringify(value_set.value), self.stringify_values(values)])
            else:
                values = queryset.filter(attribute=question.attribute).order_by('set_prefix', 'set_index', 'collection_index')
                data.append([question.attribute.uri, self.stringify_values(values)])
        
        # Workflow Documentation
        if dec[0][0] in data or dec[0][1] in data :
            # Generate Markdown File
            # Adjust raw MaRDI templates to User answers
            temp=self.dyn_template(data)
            if len(temp) == 0:
                return render(self.request,'error5.html')
            # Fill out MaRDI template
            for entry in data:
                print(entry)
                temp=re.sub("Yes: |'","",re.sub(entry[0],repr(entry[1]),temp))
            if dec[2][0] in data: 
                # Download as Markdown
                response = HttpResponse(temp, content_type="application/md")
                response['Content-Disposition'] = 'filename="workflow.md"'
                return response
            elif dec[2][1] in data and not (dec[8][0] in data or dec[8][1] in data):
                # Preview Markdown as HTML
                return HttpResponse(html_front+pypandoc.convert_text(temp,'html',format='md')+html_end)
            # Export to MaRDI Portal
            elif dec[2][1] in data and (dec[8][0] in data or dec[8][1] in data):
                '''This is a placeholder for the MaRDI Portal functionality. Until ready, documented Workflows 
                   in RDMO will be saved to a local owl ontology file.
                   Documented workflows will be new instances in Workflow class and described by three datatype 
                   properties hasMethod, hasInputData, and hasResearchObjective.'''
                # Load Ontology
                onto=get_ontology(settings.BASE_DIR+'/MaRDI_RDMO/kg/MaRDI_RDMO.owl').load()
                # Prepare new instance
                new=onto.Workflow(self.project.title)
                research_objective=''
                input_data=''
                method=''
                for entry in data:
                    if KG_export[0] in entry[0]:
                        research_objective=research_objective+entry[1]+' ; '
                    elif KG_export[1] in entry[0]:
                        method=method+entry[1]+' ; '
                    elif KG_export[2] in entry[0]:
                        input_data=input_data+entry[1]+' ; '
                new.hasResearchObjective=research_objective
                new.hasMethod=method
                new.hasInputData=input_data
                onto.save()
                return render(self.request,'export.html')

            # Not chosen
            else:
                return render(self.request,'error2.html')

        # Workflow Finding
        elif dec[1][0] in data or dec[1][1] in data:
            # Load Ontology
            onto=get_ontology(settings.BASE_DIR+'/MaRDI_RDMO/kg/MaRDI_RDMO.owl').load()
            # What to search for?
            if dec[3][0] in data or dec[3][1] in data:
                verb='hasResearchObjective'
            elif dec[4][0] in data or dec[4][1] in data:
                verb='hasMethod'
            elif dec[5][0] in data or dec[5][1] in data:
                verb='hasInputData'
            else:
                return render(self.request,'error3.html')

            # SPARQL query to get workflows and objects of interest
            workflows=list(default_world.sparql("""SELECT ?workflow ?searched_obj{ ?workflow MaRDI_RDMO:"""+verb+""" ?searched_obj . }"""))
            # List of Objects of interest
            obj=[]
            for workflow in workflows:
                obj.append(workflow[1])
            # Use TFIDF to compare user entry with available data, preprocess both before comparison
            sim_matrix = self.tfidf_similarity(self.preprocessing(obj)+self.preprocessing([data[2][1]]))
            # Index of (most likely) interesting paper.
            index=(sim_matrix-np.diag(np.diag(sim_matrix)))[-1].argmax(axis=0)
            return HttpResponse('We found a workflow that might be interesting for you:\n\n'+str(workflows[index][0])+'\n\nPlease do not forget to document your own workflow at the end so that others can benefit from it as well.',content_type="text/plain")
        
        # Not chosen
        else:
            return render(self.request,'error4.html')

    def stringify_values(self, values):
        '''Original function from csv export'''
        if values is not None:
            return '; '.join([self.stringify(value.value_and_unit) for value in values])
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
        if dec[6][0] in data or dec[6][1] in data:
            temp=math_temp
            tables=math_tables
            topics=math_topics
            ids=math_ids
        elif dec[7][0] in data or dec[7][1] in data:
            temp=exp_temp
            tables=exp_tables
            topics=exp_topics
            ids=exp_ids
        else:
            temp=[]
            return temp
        data_flat=sum(data,[])
        temp=re.sub('TEMPLATE_TITLE',self.project.title,temp)
        for n,table in enumerate(tables):
            t=self.create_table(topics[n],ids[n],sum(ids[n][0] in s for s in data_flat)+2)
            temp=re.sub(table,t,temp)
        return(temp)

    def preprocessing(self,ts):
        '''This function does a simple preprocessing of strings'''
        # Lower case, none letter removal
        ts = [re.sub(' +',' ',re.sub('[^a-z ]+',' ',t.lower())) for t in ts]
        # Stopword removal
        ts = [[w for w in t.split() if w not in set(nltk.corpus.stopwords.words('english'))] for t in ts]
        # Ending removal
        ts = [" ".join([nltk.stem.PorterStemmer().stem(w) for w in t]) for t in ts]
        return ts

    def tfidf_similarity(self,documents):
        '''This function takes a pool of documents, builds a tfidf model, 
           and determines the similarity between all documents.'''
        # Use TFIDF model
        embeddings = sk.feature_extraction.text.TfidfVectorizer().fit_transform(documents)
        # Calculate Cosine Similarities in array
        cosine_similarities = np.reshape(sk.metrics.pairwise.cosine_similarity(embeddings, embeddings).flatten(),(len(documents),len(documents)))
        return cosine_similarities
       
