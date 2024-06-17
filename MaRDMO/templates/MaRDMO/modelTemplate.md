# Title: {{ title }}

**Authors**:

- **family-names**: {{ Creator.Surname }}  
  **given-names**: {{ Creator.GivenName }}  
  {% for id in Creator.orcidID %} **orcid**:{{ id }}
  {% endfor %}
  {% for id in Creator.zbmathID %} **zbmath**:{{ id }}
  {% endfor %}
  **Date-Released**: YYYY-MM-DD  
  **Version**: Major.Minor.Patch

{% for values in AllModels.values %}

# Mathematical Model MM{{ forloop.counter }}: {{ values.Name }}

**Description**: {{ values.Description }} 
**MathModDB**:{% if values.MathModID and values.MathModID != 'not in MathModDB' %} {{ values.MathModID }} {% endif %}  
**WikiData**:{% if 'wikidata' in values.ID %} {{ values.ID|cut:"wikidata:" }} {% endif %} 
**MaRDI**:{% if 'mardi' in values.ID %} {{ values.ID|cut:"mardi:" }} {% endif %}
**Wikipedia**: {{ values.Reference }}
**Properties**: {% for value in values.Properties.values %} {% if value == IsConvex %} Is Convex {% elif value == IsNotConvex %} Is Not Convex {% elif value == IsDeterministic %} Is Deterministic {% elif value == IsStochastic %} Is Stochastic {% elif value == IsDimensionless %} Is Dimensionless {% elif value == IsDimensional %} Is Dimensional {% elif value == IsDynamic %} Is Dynamic {% elif value == IsStatic %} Is Static {% elif value == IsLinear %} Is Linear {% elif value == IsNotLinear %} Is Not Linear {% elif value == IsSpaceContinuous %} Is Space-Continuous {% elif value == IsSpaceDiscrete %} Is Space-Discrete {% elif value == IsSpaceIndependent %} Is Space-Independent {% elif value == IsTimeContinuous %} Is Time-Continuous {% elif value == IsTimeDiscrete %} Is Time-Discrete {% elif value == IsTimeIndependent %} Is Time-Independent {% endif %} {% if not forloop.last %}, {% endif %} {% endfor %}   

{% for models in values.RelationRP1.values %}
{% if forloop.counter == 1 %}

&nbsp;

**Relations to Research Problems**:

{% endif %}

models: {{ models }} 

{% endfor %}

{% for relation in values.RelationMM1.values %}
{% if forloop.counter == 1 %}

&nbsp;

**Relations to Mathematical Models**:

{% endif %}

{% if relation.0 == GeneralizedByModel %} generalized by Model: {{relation.1 }}
{% elif relation.0 == GeneralizesModel %} generalizes Model: {{relation.1 }}
{% elif relation.0 == DiscretizedByModel %} discretized by Model: {{relation.1 }}
{% elif relation.0 == DiscretizesModel %} discretizes Model: {{relation.1 }}
{% elif relation.0 == ContainedInModel %} contained in Model: {{relation.1 }}
{% elif relation.0 == ContainsModel %} contains Model: {{relation.1 }}
{% elif relation.0 == ApproximatedByModel %} approximated by Model: {{relation.1 }}
{% elif relation.0 == ApproximatesModel %} approximates Model: {{relation.1 }}
{% elif relation.0 == LinearizedByModel %} linearized by Model: {{relation.1 }}
{% elif relation.0 == LinearizesModel %} linearizes Model: {{relation.1 }}
{% elif relation.0 == SimilarToModel %} similar to Model: {{relation.1 }}
{% endif %}
{% endfor %}

## List of Mathematical Formulations

{% for values in MathematicalFormulation.values %}
{% for models in values.RelationMM1.values %}
{% if models.1 == forloop.parentloop.parentloop.counter %}

### F{{ forloop.parentloop.counter }}: {{ values.Name }}

**Description**: {{ values.Description }}
**MathModDB**:{% if values.MathModID and values.MathModID != 'not in MathModDB' %} {{ values.MathModID }} {% endif %}
**WikiData**:{% if 'wikidata' in values.ID %} {{ values.ID|cut:"wikidata:" }} {% endif %}
**MaRDI**:{% if 'mardi' in values.ID %} {{ values.ID|cut:"mardi:" }} {% endif %}

&nbsp;

**Defining formulations**: {%for value in values.Formula.values %} {{ value }} {% if not forloop.last %}, {% endif %} {% endfor %}

&nbsp;

| Symbol | Quantity | Quantity Id | Quantity Kind | Quant. Kind Id | Description | 
|:------:|:--------:|:-----------:|:-------------:|:--------------:|:-----------:|
{% for value in values.Element.values %} | {{ value.Symbol }} | {% if value.Info %} {{ value.Info.Name }} {% else %} {{ value.Quantity }} {% endif %} | {{ value.Info.QID }} | {{ value.Info.QKName }} | {{ value.Info.QKID }} | {{ value.Info.Description }} |   
{% endfor %}

&nbsp;

**Properties**:{% for value in values.Properties.values %} {% if value == IsConvex %} Is Convex {% elif value == IsNotConvex %} Is Not Convex {% elif value == IsDeterministic %} Is Deterministic {% elif value == IsStochastic %} Is Stochastic {% elif value == IsDimensionless %} Is Dimensionless {% elif value == IsDimensional %} Is Dimensional {% elif value == IsDynamic %} Is Dynamic {% elif value == IsStatic %} Is Static {% elif value == IsLinear %} Is Linear {% elif value == IsNotLinear %} Is Not Linear {% elif value == IsSpaceContinuous %} Is Space-Continuous {% elif value == IsSpaceDiscrete %} Is Space-Discrete {% elif value == IsSpaceIndependent %} Is Space-Independent {% elif value == IsTimeContinuous %} Is Time-Continuous {% elif value == IsTimeDiscrete %} Is Time-Discrete {% elif value == IsTimeIndependent %} Is Time-Independent {% endif %} {% if not forloop.last %}, {% endif %} {% endfor %}

{% for values in values.RelationMM1.values %}
{% if forloop.counter == 1 %}

&nbsp;

**Relations to Mathematical Models**: 

{% endif %}

{%if values.0 == ContainedAsAssumptionIn %} contained as Assumption in: {{ values.2 }}
{% elif values.0 == ContainedAsBoundaryConditionIn %} contained as Boundary Condition in: {{ values.2 }} 
{% elif values.0 == ContainedAsConstraintConditionIn %} contained as Constraint Condition in: {{ values.2 }} 
{% elif values.0 == ContainedAsDefintionIn %} contained as Defintion in: {{ values.2 }} 
{% elif values.0 == ContainedAsFormulationIn %} contained as Formulation in: {{ values.2 }} 
{% elif values.0 == ContainedAsInitialConditionIn %} contained as Initial Condition in: {{ values.2 }} 
{% elif values.0 == ContainedAsFinalConditionIn %} contained as Final Condition in: {{ values.2 }}
{% endif %} 
{% endfor %}

{% for values in values.RelationMF1.values %}
{% if forloop.counter == 1 %}

&nbsp;

**Relations to other Mathematical Formulations I**:

{% endif %}

{% if values.0 == ContainsAssumption %} contains as Assumption: {{ values.1 }}
{% elif values.0 == ContainedAsAssumptionIn %} contained as Assumption in: {{ values.1 }}
{% elif values.0 == ContainsAsBoundaryCondition %} contains as Boundary Condition: {{ values.1 }}
{% elif values.0 == ContainedAsBoundaryConditionIn %} contained as Boundary Condition in: {{ values.1 }} 
{% elif values.0 == ContainsAsConstraintCondition %} contains as Constraint Condition: {{ values.1 }}
{% elif values.0 == ContainedAsConstraintConditionIn %} contained as Constraint Condition in: {{ values.1 }} 
{% elif values.0 == ContainsAsDefintion %} contains as Defintion: {{ values.1 }}
{% elif values.0 == ContainedAsDefintionIn %} contained as Defintion in: {{ values.1 }} 
{% elif values.0 == ContainsAsFormulation %} contains as Formulation: {{ values.1 }}
{% elif values.0 == ContainedAsFormulationIn %} contained as Formulation in: {{ values.1 }} 
{% elif values.0 == ContainsAsInitialCondition %} contains as Initial Condition: {{ values.1 }}
{% elif values.0 == ContainedAsInitialConditionIn %} contained as Initial Condition in: {{ values.1 }} 
{% elif values.0 == ContainsAsFinalCondition %} contains as Final Condition: {{ values.1 }}
{% elif values.0 == ContainedAsFinalConditionIn %} contained as Final Condition in: {{ values.1 }}
{% endif %} 
{% endfor %}

{% for values in values.RelationMF2.values %}
{% if forloop.counter == 1 %}

&nbsp;

**Relations to other Mathematical Formulations II**:

{% endif %}

{% if values.0 == ApproximatedByFormulation %} approximated by Formulation: {{ values.1 }}
{% elif values.0 == ApproximatesFormulation %} approximates Formulation: {{ values.1 }}
{% elif values.0 == DiscretizedByFormulation %} discretized by Formulation: {{ values.1 }}
{% elif values.0 == DiscretizesFormulation %} discretizes Formulation: {{ values.1 }}
{% elif values.0 == GeneralizedByFormulation %} generalized by Formulation: {{ values.1 }}
{% elif values.0 == GeneralizesFormulation %} generalizes Formulation: {{ values.1 }}
{% elif values.0 == NondimensionalizedByFormulation %} nondimensionalized by Formulation: {{ values.1 }}
{% elif values.0 == NondimensionalzesFormulation %} nondimensionalizes Formulation: {{ values.1 }}
{% elif values.0 == LinearizedByFormulation %} linearized by Formulation: {{ values.1 }}
{% elif values.0 == LinearizesFormulation %} linearizes Formulation: {{ values.1 }}
{% elif values.0 == SimilarToFormulation %} similar to Formulation: {{ values.1 }}
{% endif %}
{% endfor %}

{% endif %}
{% endfor %}
{% endfor %}
{% endfor %}

# Task

{% for values in Task.values %}

## Task T{{ forloop.counter }}: {{ values.Name }}

**Description**: {{ values.Description }}
**MathModDB**:{% if values.MathModID and values.MathModID != 'not in MathModDB' %} {{ values.MathModID }} {% endif %}  
**WikiData**:{% if 'wikidata' in values.ID %} {{ values.ID|cut:"wikidata:" }} {% endif %}
**MaRDI**:{% if 'mardi' in values.ID %} {{ values.ID|cut:"mardi:" }} {% endif %} 
**Wikipedia**: {{ values.Reference }}
**Properties**: {% for value in values.Properties.values %} {% if value == IsLinear %} Is Linear {% elif value == IsNotLinear %} Is Not Linear {% endif %} {% if not forloop.last %}, {% endif %} {% endfor %}  
**Task Type**: {% for value in values.TaskClass.values %} {% if value == ComputationalTask %} Computational Task {% endif %} {% endfor %}

{% for value in values.RelationRP.values %}
{% if forloop.counter == 1 %}

&nbsp;

**Relations to Research Problems**

{% endif %}

contained in Research Problem: {{ value }}

{% endfor %}


{% for value in values.RelationMM.values %}
{% if forloop.counter == 1 %}

&nbsp;

**Relations to Mathematical Models**

{% endif %}

applies Mathematical Model: {{ value }}

{% endfor %}

{% for value in values.RelationQQK.values %}
{% if forloop.counter == 1 %}

&nbsp;

**Relations to Quantities / Quantity Kinds**

{% endif %}

{% if value.0 == ContainsAsInput2 %} contains Input: {{ value.1 }}
{% elif value.0 == ContainsAsOutput2 %} contains Output: {{ value.1 }}
{% elif value.0 == ContainsAsObjective2 %} contains Objective: {{ value.1 }}
{% elif value.0 == ContainsAsParameter2 %} contains Parameter: {{ value.1 }}
{% endif %}
{% endfor %}

{% for value in values.RelationT.values %}
{% if forloop.counter == 1 %}

&nbsp;

**Relations to Tasks**

{% endif %}

{% if value.0 == GeneralizedByTask %} generalized by Task: {{ value.1 }}
{% elif value.0 == GeneralizesTask %} generalizes Task: {{ value.1 }}
{% elif value.0 == DiscretizedByTask %} discretized by Task: {{ value.1 }}
{% elif value.0 == DiscretizesTask %} discretizes Task: {{ value.1 }}
{% elif value.0 == ApproximatedByTask %} approximated by Task: {{ value.1 }}
{% elif value.0 == ApproximatesTask %} approximates Task: {{ value.1 }}
{% elif value.0 == LinearizedByTask %} linearized by Task: {{ value.1 }}
{% elif value.0 == LinearizesTask %} linearizes Task: {{ value.1 }}
{% elif value.0 == SimilarToTask %} similar to Task: {{ value.1 }}
{% endif %}
{% endfor %}

## List of Mathematical Formulations

{% for values in MathematicalFormulation.values %}
{% for tasks in values.RelationT1.values %}
{% if tasks.1 == forloop.parentloop.parentloop.counter %}

### F{{ forloop.parentloop.counter }}: {{ values.Name }}

**Description**: {{ values.Description }}
**MathModDB**:{% if values.MathModID and values.MathModID != 'not in MathModDB' %} {{ values.MathModID }} {% endif %}
**WikiData**:{% if 'wikidata' in values.ID %} {{ values.ID|cut:"wikidata:" }} {% endif %}
**MaRDI**:{% if 'mardi' in values.ID %} {{ values.ID|cut:"mardi:" }} {% endif %}

&nbsp;

**Defining formulations**: {%for value in values.Formula.values %} {{ value }} {% if not forloop.last %}, {% endif %} {% endfor %}

&nbsp;

| Symbol | Quantity | Quantity Id | Quantity Kind | Quant. Kind Id | Description |
|:------:|:--------:|:-----------:|:-------------:|:--------------:|:-----------:|
{% for value in values.Element.values %} | {{ value.Symbol }} | {% if value.Info %} {{ value.Info.Name }} {% else %} {{ value.Quantity }} {% endif %} | {{ value.Info.QID }} | {{ value.Info.QKName }} | {{ value.Info.QKID }} | {{ value.Info.Description }} |
{% endfor %}

&nbsp;

**Properties**:{% for value in values.Properties.values %} {% if value == IsConvex %} Is Convex {% elif value == IsNotConvex %} Is Not Convex {% elif value == IsDeterministic %} Is Deterministic {% elif value == IsStochastic %} Is Stochastic {% elif value == IsDimensionless %} Is Dimensionless {% elif value == IsDimensional %} Is Dimensional {% elif value == IsDynamic %} Is Dynamic {% elif value == IsStatic %} Is Static {% elif value == IsLinear %} Is Linear {% elif value == IsNotLinear %} Is Not Linear {% elif value == IsSpaceContinuous %} Is Space-Continuous {% elif value == IsSpaceDiscrete %} Is Space-Discrete {% elif value == IsSpaceIndependent %} Is Space-Independent {% elif value == IsTimeContinuous %} Is Time-Continuous {% elif value == IsTimeDiscrete %} Is Time-Discrete {% elif value == IsTimeIndependent %} Is Time-Independent {% endif %} {% if not forloop.last %}, {% endif %} {% endfor %}

{% for values in values.RelationT1.values %}
{% if forloop.counter == 1 %}

&nbsp;

**Relations to Tasks**:

{% endif %}

{% if values.0 == ContainedAsAssumptionIn %} contained as Assumption in: {{ values.2 }}
{% elif values.0 == ContainedAsBoundaryConditionIn %} contained as Boundary Condition in: {{ values.2 }}
{% elif values.0 == ContainedAsConstraintConditionIn %} contained as Constraint Condition in: {{ values.2 }}
{% elif values.0 == ContainedAsDefinitionIn %} contained as Definition in: {{ values.2 }}
{% elif values.0 == ContainedAsFormulationIn %} contained as Formulation in: {{ values.2 }}
{% elif values.0 == ContainedAsInitialConditionIn %} contained as Initial Condition in: {{ values.2 }}
{% elif values.0 == ContainedAsFinalConditionIn %} contained as Final Condition in: {{ values.2 }}
{% elif values.0 == ContainedAsInputIn %} contained as Input in: {{ values.2 }}
{% elif values.0 == ContainedAsOutputIn %} contained as Output in: {{ values.2 }}
{% elif values.0 == ContainedAsObjectiveIn %} contained as Objective in: {{ values.2 }}
{% elif values.0 == ContainedAsParameterIn %} contained as Parameter in: {{ values.2 }}
{% endif %}
{% endfor %}


{% for values in values.RelationMM1.values %}
{% if forloop.counter == 1 %}

&nbsp;

**Relations to Mathematical Models**:

{% endif %}

{%if values.0 == ContainedAsAssumptionIn %} contained as Assumption in: {{ values.2 }}
{% elif values.0 == ContainedAsBoundaryConditionIn %} contained as Boundary Condition in: {{ values.2 }}
{% elif values.0 == ContainedAsConstraintConditionIn %} contained as Constraint Condition in: {{ values.2 }}
{% elif values.0 == ContainedAsDefintionIn %} contained as Defintion in: {{ values.2 }}
{% elif values.0 == ContainedAsFormulationIn %} contained as Formulation in: {{ values.2 }}
{% elif values.0 == ContainedAsInitialConditionIn %} contained as Initial Condition in: {{ values.2 }}
{% elif values.0 == ContainedAsFinalConditionIn %} contained as Final Condition in: {{ values.2 }}
{% endif %}
{% endfor %}

{% for values in values.RelationMF1.values %}
{% if forloop.counter == 1 %}

&nbsp;

**Relations to other Mathematical Formulations I**:

{% endif %}

{% if values.0 == ContainsAssumption %} contains as Assumption: {{ values.1 }}
{% elif values.0 == ContainedAsAssumptionIn %} contained as Assumption in: {{ values.1 }}
{% elif values.0 == ContainsAsBoundaryCondition %} contains as Boundary Condition: {{ values.1 }}
{% elif values.0 == ContainedAsBoundaryConditionIn %} contained as Boundary Condition in: {{ values.1 }}
{% elif values.0 == ContainsAsConstraintCondition %} contains as Constraint Condition: {{ values.1 }}
{% elif values.0 == ContainedAsConstraintConditionIn %} contained as Constraint Condition in: {{ values.1 }}
{% elif values.0 == ContainsAsDefintion %} contains as Defintion: {{ values.1 }}
{% elif values.0 == ContainedAsDefintionIn %} contained as Defintion in: {{ values.1 }}
{% elif values.0 == ContainsAsFormulation %} contains as Formulation: {{ values.1 }}
{% elif values.0 == ContainedAsFormulationIn %} contained as Formulation in: {{ values.1 }}
{% elif values.0 == ContainsAsInitialCondition %} contains as Initial Condition: {{ values.1 }}
{% elif values.0 == ContainedAsInitialConditionIn %} contained as Initial Condition in: {{ values.1 }}
{% elif values.0 == ContainsAsFinalCondition %} contains as Final Condition: {{ values.1 }}
{% elif values.0 == ContainedAsFinalConditionIn %} contained as Final Condition in: {{ values.1 }}
{% endif %}
{% endfor %}

{% for values in values.RelationMF2.values %}
{% if forloop.counter == 1 %}

&nbsp;

**Relations to other Mathematical Formulations II**:

{% endif %}

{% if values.0 == ApproximatedByFormulation %} approximated by Formulation: {{ values.1 }}
{% elif values.0 == ApproximatesFormulation %} approximates Formulation: {{ values.1 }}
{% elif values.0 == DiscretizedByFormulation %} discretized by Formulation: {{ values.1 }}
{% elif values.0 == DiscretizesFormulation %} discretizes Formulation: {{ values.1 }}
{% elif values.0 == GeneralizedByFormulation %} generalized by Formulation: {{ values.1 }}
{% elif values.0 == GeneralizesFormulation %} generalizes Formulation: {{ values.1 }}
{% elif values.0 == NondimensionalizedByFormulation %} nondimensionalized by Formulation: {{ values.1 }}
{% elif values.0 == NondimensionalzesFormulation %} nondimensionalizes Formulation: {{ values.1 }}
{% elif values.0 == LinearizedByFormulation %} linearized by Formulation: {{ values.1 }}
{% elif values.0 == LinearizesFormulation %} linearizes Formulation: {{ values.1 }}
{% elif values.0 == SimilarToFormulation %} similar to Formulation: {{ values.1 }}
{% endif %}
{% endfor %}

{% endif %}
{% endfor %}
{% endfor %}

{% endfor %}

# Publication

{% for values in PublicationModel.values %}

## P{{ forloop.counter }}: {{ values.Name }}

MathModID:{% if values.MathModID and values.MathModID != 'not in MathModDB' %} {{ values.MathModID }} {% endif %}
DOI:{% if 'doi' in values.Reference %} {{ values.Reference|cut:"doi:" }} {% endif %}   
URL:{% if 'url' in values.Reference %} {{ values.Reference|cut:"url:" }} {% endif %}  

{% for values in values.RelationP.values %}
{% if forloop.counter == 1 %}

&nbsp;

**Relations to Entities of the Mathematical Model(s)**:

{% endif %}

{% if values.0 == Documents %} documents: {{ values.1 }}
{% elif values.0 == Invents %} invents: {{ values.1 }}
{% elif values.0 == Studies %} studies: {{ values.1 }}
{% elif values.0 == Surveys %} surveys: {{ values.1 }}
{% elif values.0 == Uses %} uses: {{ values.1 }}
{% endif %}
{% endfor %}
{% endfor %}

# Research Field

{% for values in ResearchField.values %}

## RF{{ forloop.counter }}: {{ values.Name }}

**Description**: {{ values.Description }}
**MathModDB**:{% if values.MathModID and values.MathModID != 'not in MathModDB' %} {{ values.MathModID }} {% endif %} 
**WikiData**:{% if 'wikidata' in values.ID %} {{ values.ID|cut:"wikidata:" }} {% endif %}   
**MaRDI**:{% if 'mardi' in values.ID %} {{ values.ID|cut:"mardi:" }} {% endif %}

{% for relation in values.RelationRF1.values %}
{% if forloop.counter == 1 %}

&nbsp;

**Relations to other Research Fields**:

{% endif %}

{% if relation.0 == GeneralizedByField %} generalized by Field: {{relation.1 }} 
{% elif relation.0 == GeneralizesField %} generalizes Field: {{relation.1 }}
{% elif relation.0 == SimilarToField %} similar to Field: {{relation.1 }}
{% endif %}
{% endfor %} 

{% endfor %}

# Research Problem

{% for values in ResearchProblem.values %}

## RP{{ forloop.counter }}: {{ values.Name }}

**Description**: {{ values.Description }}
**DOI**:{{ values.Reference|cut:"doi:" }}  
**MathModDB**:{% if values.MathModID and values.MathModID != 'not in MathModDB' %} {{ values.MathModID }} {% endif %}
**WikiData**:{% if 'wikidata' in values.ID %} {{ values.ID|cut:"wikidata:" }} {% endif %} 
**MaRDI**:{% if 'mardi' in values.ID %} {{ values.ID|cut:"mardi:" }} {% endif %} 

{% for researchfield in values.RelationRF1.values %}
{% if forloop.counter == 1 %}

&nbsp;

**Relations to Research Fields**:

{% endif %}

contained in Field: {{ researchfield }}
{% endfor %}

{% for relation in values.RelationRP1.values %}
{% if forloop.counter == 1 %}
&nbsp;

**Relations to other Research Problems**:

{% endif %}

{% if relation.0 == GeneralizedByProblem %} generalized by Problem: {{relation.1 }}
{% elif relation.0 == GeneralizesProblem %} generalizes Problem: {{relation.1 }}
{% elif relation.0 == SimilarToProblem %} similar to Problem: {{relation.1 }}
{% endif %}
{% endfor %}

{% endfor %}

# Quantity

{% for values in Quantity_refined.values %}

## Q{{ forloop.counter }}: {{ values.QName }}

**Description**: {{ values.QDescription }}
**DOI**:{% if 'doi' in values.ID %} {{ values.ID|cut:"doi:" }} {% endif %}
**MathModDB**:{% if values.MathModID and values.MathModID != 'not in MathModDB' %} {{ values.MathModID }} {% endif %}
**WikiData**:{% if 'wikidata' in values.ID %} {{ values.ID|cut:"wikidata:" }} {% endif %}
**MaRDI**:{% if 'mardi' in values.ID %} {{ values.ID|cut:"mardi:" }} {% endif %}
**Properties**: {% for value in values.QProperties.values %} {% if value == IsDimensionless %} Is Dimensionless {% elif value == IsDimensional %} Is Dimensional {% elif value == IsLinear %} Is Linear {% elif value == IsNotLinear %} Is Not Linear {% endif %} {% if not forloop.last %}, {% endif %}{% endfor %}

{% for values in values.RelationQQ.values %}
{% if forloop.counter == 1 %}
&nbsp;

**Relations to other Quantities**:

{% endif %}

{% if values.0 == GeneralizedByQuantity %} generalized by Quantity: {{ values.1 }}
{% elif values.0 == GeneralizesQuantity %} generalizes Quantity: {{ values.1 }}
{% elif values.0 == ApproximatedByQuantity %} approximated by Quantity: {{ values.1 }}
{% elif values.0 == ApproximatesQuantity %} approximates Quantity: {{ values.1 }}
{% elif values.0 == LinearizedByQuantity %} linearized by Quantity: {{ values.1 }}
{% elif values.0 == LinearizesQuantity %} linearizes Quantity: {{ values.1 }}
{% elif values.0 == NondimensionalizedByQuantity %} nondimensionalized by Quantity: {{ values.1 }}
{% elif values.0 == NondimensionalizesQuantity %} nondimensionalizes Quantity: {{ values.1 }}
{% elif values.0 == SimilarToQuantity %} similar to Quantity: {{ values.1 }}
{% endif %}
{% endfor %}

{% for values in values.RelationQQK.values %}
{% if forloop.counter == 1 %}
&nbsp;

**Relations to Quantity Kinds**:

{% endif %}

{% if values.0 == GeneralizedByQuantityKind %} generalized by Quantity Kind: {{ values.1 }}
{% elif values.0 == GeneralizesQuantityKind %} generalizes Quantity Kind: {{ values.1 }}
{% elif values.0 == NondimensionalizedByQuantityKind %} nondimensionalized by Quantity Kind: {{ values.1 }}
{% elif values.0 == NondimensionalizesQuantityKind %} nondimensionalizes Quantity Kind: {{ values.1 }}
{% elif values.0 == SimilarToQuantityKind %} similar to Quantity Kind: {{ values.1 }}
{% endif %}
{% endfor %}

{% if values.MDef %}

#Definition

**Name**: {{ values.MDef.Name }}
**Description**: {{ values.MDef.Description }}
**MathModDB**:{% if values.MDef.MathModID and values.MDef.MathModID != 'not in MathModDB' %} {{ values.MDef.MathModID }} {% endif %}
**WikiData**:{% if 'wikidata' in values.MDef.ID %} {{ values.MDef.ID|cut:"wikidata:" }} {% endif %}
**MaRDI**:{% if 'mardi' in values.MDef.ID %} {{ values.MDef.ID|cut:"mardi:" }} {% endif %}

&nbsp;

**Defining formulations**: {%for value in values.MDef.Formula.values %} {{ value }} {% if not forloop.last %}, {% endif %} {% endfor %}

&nbsp;

| Symbol | Quantity | Quantity Id | Quantity Kind | Quant. Kind Id | Description |
|:------:|:--------:|:-----------:|:-------------:|:--------------:|:-----------:|
{% for value in values.MDef.Element.values %} | {{ value.Symbol }} | {% if value.Info %} {{ value.Info.Name }} {% else %} {{ value.Quantity }} {% endif %} | {{ value.Info.QID }} | {{ value.Info.QKName }} | {{ value.Info.QKID }} | {{ value.Info.Description }} |
{% endfor %}

&nbsp;

**Properties**:{% for value in values.Properties.values %} {% if value == IsConvex %} Is Convex {% elif value == IsNotConvex %} Is Not Convex {% elif value == IsDeterministic %} Is Deterministic {% elif value == IsStochastic %} Is Stochastic {% elif value == IsDimensionless %} Is Dimensionless {% elif value == IsDimensional %} Is Dimensional {% elif value == IsDynamic %} Is Dynamic {% elif value == IsStatic %} Is Static {% elif value == IsLinear %} Is Linear {% elif value == IsNotLinear %} Is Not Linear {% elif value == IsSpaceContinuous %} Is Space-Continuous {% elif value == IsSpaceDiscrete %} Is Space-Discrete {% elif value == IsSpaceIndependent %} Is Space-Independent {% elif value == IsTimeContinuous %} Is Time-Continuous {% elif value == IsTimeDiscrete %} Is Time-Discrete {% elif value == IsTimeIndependent %} Is Time-Independent {% endif %} {% if not forloop.last %}, {% endif %} {% endfor %}

{% endif %}
{% endfor %}

# Quantity Kind

{% for values in QuantityKind_refined.values %}

## QK{{ forloop.counter }}: {{ values.QKName }}

**Description**: {{ values.QKDescription }}
**DOI**:{% if 'doi' in values.ID %} {{ values.ID|cut:"doi:" }} {% endif %}
**MathModDB**:{% if values.MathModID and values.MathModID != 'not in MathModDB' %} {{ values.MathModID }} {% endif %}
**WikiData**:{% if 'wikidata' in values.ID %} {{ values.ID|cut:"wikidata:" }} {% endif %}
**MaRDI**:{% if 'mardi' in values.ID %} {{ values.ID|cut:"mardi:" }} {% endif %}
**Properties**: {% for value in values.QKProperties.values %} {% if value == IsDimensionless %} Is Dimensionless {% elif value == IsDimensional %} Is Dimensional {% endif %} {% if not forloop.last %}, {% endif %}{% endfor %}

{% for values in values.RelationQKQK.values %}
{% if forloop.counter == 1 %}
&nbsp;

**Relations to other Quantity Kinds**:

{% endif %}

{% if values.0 == GeneralizedByQuantityKind %} generalized by Quantity Kind: {{ values.1 }}
{% elif values.0 == GeneralizesQuantityKind %} generalizes Quantity Kind: {{ values.1 }}
{% elif values.0 == NondimensionalizedByQuantityKind %} nondimensionalized by Quantity Kind: {{ values.1 }}
{% elif values.0 == NondimensionalizesQuantityKind %} nondimensionalizes Quantity Kind: {{ values.1 }}
{% elif values.0 == SimilarToQuantityKind %} similar to Quantity Kind: {{ values.1 }}
{% endif %}
{% endfor %}

{% for values in values.RelationQKQ.values %}
{% if forloop.counter == 1 %}
&nbsp;

**Relations to Quantities**:

{% endif %}

{% if values.0 == GeneralizedByQuantityKind %} generalized by Quantity: {{ values.1 }}
{% elif values.0 == GeneralizesQuantityKind %} generalizes Quantity: {{ values.1 }}
{% elif values.0 == NondimensionalizedByQuantityKind %} nondimensionalized by Quantity: {{ values.1 }}
{% elif values.0 == NondimensionalizesQuantityKind %} nondimensionalizes Quantity: {{ values.1 }}
{% elif values.0 == SimilarToQuantityKind %} similar to Quantity: {{ values.1 }}
{% endif %}
{% endfor %}

{% endfor %}
