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

{% for values in MathematicalModel.values %}

# Mathematical Model MM{{ forloop.counter }}: {{ values.Name }}

**Description**: {{ values.Description }} 
**MathModDB**:{% if values.MathModID and values.MathModID != 'not in MathModDB' %} {{ values.MathModID }} {% endif %}  
**WikiData**:{% if 'wikidata' in values.ID %} {{ values.ID|cut:"wikidata:" }} {% endif %} 
**MaRDI**:{% if 'mardi' in values.ID %} {{ values.ID|cut:"mardi:" }} {% endif %}
**Properties**: {% for value in values.Properties.values %} {% if value == isConvex %} Is Convex {% elif value == isNotConvex %} Is Not Convex {% elif value == isDeterministic %} Is Deterministic {% elif value == isStochastic %} Is Stochastic {% elif value == isDimensionless %} Is Dimensionless {% elif value == isDimensional %} Is Dimensional {% elif value == isDynamic %} Is Dynamic {% elif value == isStatic %} Is Static {% elif value == isLinear %} Is Linear {% elif value == isNotLinear %} Is Not Linear {% elif value == isSpaceContinuous %} Is Space-Continuous {% elif value == isSpaceDiscrete %} Is Space-Discrete {% elif value == isSpaceIndependent %} Is Space-Independent {% elif value == isTimeContinuous %} Is Time-Continuous {% elif value == isTimeDiscrete %} Is Time-Discrete {% elif value == isTimeIndependent %} Is Time-Independent {% endif %} {% if not forloop.last %}, {% endif %} {% endfor %}   

{% for models in values.RelationRP1.values %}
{% if forloop.counter == 1 %}

&nbsp;

**Relations to Research Problems**:

{% endif %}

models: {{ models.1 }} 

{% endfor %}

{% for relation in values.RelationMM1.values %}
{% if forloop.counter == 1 %}

&nbsp;

**Relations to Mathematical Models**:

{% endif %}

{% if relation.0 == generalizedByModel %} generalized by Model: {{relation.1 }}
{% elif relation.0 == generalizesModel %} generalizes Model: {{relation.1 }}
{% elif relation.0 == discretizedByModel %} discretized by Model: {{relation.1 }}
{% elif relation.0 == discretizesModel %} discretizes Model: {{relation.1 }}
{% elif relation.0 == containedInModel %} contained in Model: {{relation.1 }}
{% elif relation.0 == containsModel %} contains Model: {{relation.1 }}
{% elif relation.0 == approximatedByModel %} approximated by Model: {{relation.1 }}
{% elif relation.0 == approximatesModel %} approximates Model: {{relation.1 }}
{% elif relation.0 == linearizedByModel %} linearized by Model: {{relation.1 }}
{% elif relation.0 == linearizesModel %} linearizes Model: {{relation.1 }}
{% elif relation.0 == similarToModel %} similar to Model: {{relation.1 }}
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

**Properties**:{% for value in values.Properties.values %} {% if value == isConvex %} Is Convex {% elif value == isNotConvex %} Is Not Convex {% elif value == isDeterministic %} Is Deterministic {% elif value == isStochastic %} Is Stochastic {% elif value == isDimensionless %} Is Dimensionless {% elif value == isDimensional %} Is Dimensional {% elif value == isDynamic %} Is Dynamic {% elif value == isStatic %} Is Static {% elif value == isLinear %} Is Linear {% elif value == isNotLinear %} Is Not Linear {% elif value == isSpaceContinuous %} Is Space-Continuous {% elif value == isSpaceDiscrete %} Is Space-Discrete {% elif value == isSpaceIndependent %} Is Space-Independent {% elif value == isTimeContinuous %} Is Time-Continuous {% elif value == isTimeDiscrete %} Is Time-Discrete {% elif value == isTimeIndependent %} Is Time-Independent {% endif %} {% if not forloop.last %}, {% endif %} {% endfor %}

{% for values in values.RelationMM1.values %}
{% if forloop.counter == 1 %}

&nbsp;

**Relations to Mathematical Models**: 

{% endif %}

{%if values.0 == containedAsAssumptionIn %} contained as Assumption in: {{ values.2 }}
{% elif values.0 == containedAsBoundaryConditionIn %} contained as Boundary Condition in: {{ values.2 }} 
{% elif values.0 == containedAsConstraintConditionIn %} contained as Constraint Condition in: {{ values.2 }} 
{% elif values.0 == containedAsCouplingConditionIn %} contained as Coupling Condition in: {{ values.2 }} 
{% elif values.0 == containedAsFormulationIn %} contained as Formulation in: {{ values.2 }} 
{% elif values.0 == containedAsInitialConditionIn %} contained as Initial Condition in: {{ values.2 }} 
{% elif values.0 == containedAsFinalConditionIn %} contained as Final Condition in: {{ values.2 }}
{% endif %} 
{% endfor %}

{% for values in values.RelationMF1.values %}
{% if forloop.counter == 1 %}

&nbsp;

**Relations to other Mathematical Formulations I**:

{% endif %}

{% if values.0 == containsAssumption %} contains as Assumption: {{ values.1 }}
{% elif values.0 == containedAsAssumptionIn %} contained as Assumption in: {{ values.1 }}
{% elif values.0 == containsBoundaryCondition %} contains as Boundary Condition: {{ values.1 }}
{% elif values.0 == containedAsBoundaryConditionIn %} contained as Boundary Condition in: {{ values.1 }} 
{% elif values.0 == containsConstraintCondition %} contains as Constraint Condition: {{ values.1 }}
{% elif values.0 == containedAsConstraintConditionIn %} contained as Constraint Condition in: {{ values.1 }} 
{% elif values.0 == containsCouplingCondition %} contains as Coupling Condition: {{ values.1 }}
{% elif values.0 == containedAsCouplingConditionIn %} contained as Coupling Condition in: {{ values.1 }} 
{% elif values.0 == containsFormulation %} contains as Formulation: {{ values.1 }}
{% elif values.0 == containedAsFormulationIn %} contained as Formulation in: {{ values.1 }} 
{% elif values.0 == containsInitialCondition %} contains as Initial Condition: {{ values.1 }}
{% elif values.0 == containedAsInitialConditionIn %} contained as Initial Condition in: {{ values.1 }} 
{% elif values.0 == containsFinalCondition %} contains as Final Condition: {{ values.1 }}
{% elif values.0 == containedAsFinalConditionIn %} contained as Final Condition in: {{ values.1 }}
{% endif %} 
{% endfor %}

{% for values in values.RelationMF2.values %}
{% if forloop.counter == 1 %}

&nbsp;

**Relations to other Mathematical Formulations II**:

{% endif %}

{% if values.0 == approximatedByFormulation %} approximated by Formulation: {{ values.1 }}
{% elif values.0 == approximatesFormulation %} approximates Formulation: {{ values.1 }}
{% elif values.0 == discretizedByFormulation %} discretized by Formulation: {{ values.1 }}
{% elif values.0 == discretizesFormulation %} discretizes Formulation: {{ values.1 }}
{% elif values.0 == generalizedByFormulation %} generalized by Formulation: {{ values.1 }}
{% elif values.0 == generalizesFormulation %} generalizes Formulation: {{ values.1 }}
{% elif values.0 == nondimensionalizedByFormulation %} nondimensionalized by Formulation: {{ values.1 }}
{% elif values.0 == nondimensionalzesFormulation %} nondimensionalizes Formulation: {{ values.1 }}
{% elif values.0 == linearizedByFormulation %} linearized by Formulation: {{ values.1 }}
{% elif values.0 == linearizesFormulation %} linearizes Formulation: {{ values.1 }}
{% elif values.0 == similarToFormulation %} similar to Formulation: {{ values.1 }}
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
**MathModDB**:{% if 'mathmoddb' in values.ID %} {{ values.ID|cut:"mathmoddb:" }} {% endif %}  
**WikiData**:{% if 'wikidata' in values.ID %} {{ values.ID|cut:"wikidata:" }} {% endif %}
**MaRDI**:{% if 'mardi' in values.ID %} {{ values.ID|cut:"mardi:" }} {% endif %} 
**Properties**: {% for value in values.Properties.values %} {% if value == isLinear %} Is Linear {% elif value == isNotLinear %} Is Not Linear {% endif %} {% if not forloop.last %}, {% endif %} {% endfor %}  
**Task Type**: {% for value in values.TaskClass.values %} {% if value == ComputationalTask %} Computational Task {% endif %} {% endfor %}

{% for value in values.RelationMM.values %}
{% if forloop.counter == 1 %}

&nbsp;

**Relations to Mathematical Models**

{% endif %}

applies Mathematical Model: {{ value.1 }}

{% endfor %}

{% for value in values.RelationQQK.values %}
{% if forloop.counter == 1 %}

&nbsp;

**Relations to Quantities / Quantity Kinds**

{% endif %}

{% if value.0 == containsInput %} contains Input: {{ value.1 }}
{% elif value.0 == containsOutput %} contains Output: {{ value.1 }}
{% elif value.0 == containsObjective %} contains Objective: {{ value.1 }}
{% elif value.0 == containsParameter %} contains Parameter: {{ value.1 }}
{% elif value.0 == containsConstant %} contains Constant: {{ value.1 }}
{% endif %}
{% endfor %}

{% for value in values.RelationT.values %}
{% if forloop.counter == 1 %}

&nbsp;

**Relations to Tasks**

{% endif %}

{% if value.0 == generalizedByTask %} generalized by Task: {{ value.1 }}
{% elif value.0 == generalizesTask %} generalizes Task: {{ value.1 }}
{% elif value.0 == discretizedByTask %} discretized by Task: {{ value.1 }}
{% elif value.0 == discretizesTask %} discretizes Task: {{ value.1 }}
{% elif value.0 == containedInTask %} contained in Task: {{ value.1 }}
{% elif value.0 == containsTask %} contains Task: {{ value.1 }}
{% elif value.0 == approximatedByTask %} approximated by Task: {{ value.1 }}
{% elif value.0 == approximatesTask %} approximates Task: {{ value.1 }}
{% elif value.0 == linearizedByTask %} linearized by Task: {{ value.1 }}
{% elif value.0 == linearizesTask %} linearizes Task: {{ value.1 }}
{% elif value.0 == similarToTask %} similar to Task: {{ value.1 }}
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

**Properties**:{% for value in values.Properties.values %} {% if value == isConvex %} Is Convex {% elif value == isNotConvex %} Is Not Convex {% elif value == isDeterministic %} Is Deterministic {% elif value == isStochastic %} Is Stochastic {% elif value == isDimensionless %} Is Dimensionless {% elif value == isDimensional %} Is Dimensional {% elif value == isDynamic %} Is Dynamic {% elif value == isStatic %} Is Static {% elif value == isLinear %} Is Linear {% elif value == isNotLinear %} Is Not Linear {% elif value == isSpaceContinuous %} Is Space-Continuous {% elif value == isSpaceDiscrete %} Is Space-Discrete {% elif value == isSpaceIndependent %} Is Space-Independent {% elif value == isTimeContinuous %} Is Time-Continuous {% elif value == isTimeDiscrete %} Is Time-Discrete {% elif value == isTimeIndependent %} Is Time-Independent {% endif %} {% if not forloop.last %}, {% endif %} {% endfor %}

{% for values in values.RelationT1.values %}
{% if forloop.counter == 1 %}

&nbsp;

**Relations to Tasks**:

{% endif %}

{% if values.0 == containedAsAssumptionIn %} contained as Assumption in: {{ values.2 }}
{% elif values.0 == containedAsBoundaryConditionIn %} contained as Boundary Condition in: {{ values.2 }}
{% elif values.0 == containedAsConstraintConditionIn %} contained as Constraint Condition in: {{ values.2 }}
{% elif values.0 == containedAsDefinitionIn %} contained as Definition in: {{ values.2 }}
{% elif values.0 == containedAsFormulationIn %} contained as Formulation in: {{ values.2 }}
{% elif values.0 == containedAsInitialConditionIn %} contained as Initial Condition in: {{ values.2 }}
{% elif values.0 == containedAsFinalConditionIn %} contained as Final Condition in: {{ values.2 }}
{% endif %}
{% endfor %}


{% for values in values.RelationMM1.values %}
{% if forloop.counter == 1 %}

&nbsp;

**Relations to Mathematical Models**:

{% endif %}

{%if values.0 == containedAsAssumptionIn %} contained as Assumption in: {{ values.2 }}
{% elif values.0 == containedAsBoundaryConditionIn %} contained as Boundary Condition in: {{ values.2 }}
{% elif values.0 == containedAsConstraintConditionIn %} contained as Constraint Condition in: {{ values.2 }}
{% elif values.0 == containedAsDefintionIn %} contained as Defintion in: {{ values.2 }}
{% elif values.0 == containedAsFormulationIn %} contained as Formulation in: {{ values.2 }}
{% elif values.0 == containedAsInitialConditionIn %} contained as Initial Condition in: {{ values.2 }}
{% elif values.0 == containedAsFinalConditionIn %} contained as Final Condition in: {{ values.2 }}
{% endif %}
{% endfor %}

{% for values in values.RelationMF1.values %}
{% if forloop.counter == 1 %}

&nbsp;

**Relations to other Mathematical Formulations I**:

{% endif %}

{% if values.0 == containsAssumption %} contains as Assumption: {{ values.1 }}
{% elif values.0 == containedAsAssumptionIn %} contained as Assumption in: {{ values.1 }}
{% elif values.0 == containsBoundaryCondition %} contains as Boundary Condition: {{ values.1 }}
{% elif values.0 == containedAsBoundaryConditionIn %} contained as Boundary Condition in: {{ values.1 }}
{% elif values.0 == containsConstraintCondition %} contains as Constraint Condition: {{ values.1 }}
{% elif values.0 == containedAsConstraintConditionIn %} contained as Constraint Condition in: {{ values.1 }}
{% elif values.0 == containsCouplingCondition %} contains as Coupling Condition: {{ values.1 }}
{% elif values.0 == containedAsCouplingConditionIn %} contained as Coupling Condition in: {{ values.1 }}
{% elif values.0 == containsFormulation %} contains as Formulation: {{ values.1 }}
{% elif values.0 == containedAsFormulationIn %} contained as Formulation in: {{ values.1 }}
{% elif values.0 == containsInitialCondition %} contains as Initial Condition: {{ values.1 }}
{% elif values.0 == containedAsInitialConditionIn %} contained as Initial Condition in: {{ values.1 }}
{% elif values.0 == containsFinalCondition %} contains as Final Condition: {{ values.1 }}
{% elif values.0 == containedAsFinalConditionIn %} contained as Final Condition in: {{ values.1 }}
{% endif %}
{% endfor %}

{% for values in values.RelationMF2.values %}
{% if forloop.counter == 1 %}

&nbsp;

**Relations to other Mathematical Formulations II**:

{% endif %}

{% if values.0 == approximatedByFormulation %} approximated by Formulation: {{ values.1 }}
{% elif values.0 == approximatesFormulation %} approximates Formulation: {{ values.1 }}
{% elif values.0 == discretizedByFormulation %} discretized by Formulation: {{ values.1 }}
{% elif values.0 == discretizesFormulation %} discretizes Formulation: {{ values.1 }}
{% elif values.0 == generalizedByFormulation %} generalized by Formulation: {{ values.1 }}
{% elif values.0 == generalizesFormulation %} generalizes Formulation: {{ values.1 }}
{% elif values.0 == nondimensionalizedByFormulation %} nondimensionalized by Formulation: {{ values.1 }}
{% elif values.0 == nondimensionalzesFormulation %} nondimensionalizes Formulation: {{ values.1 }}
{% elif values.0 == linearizedByFormulation %} linearized by Formulation: {{ values.1 }}
{% elif values.0 == linearizesFormulation %} linearizes Formulation: {{ values.1 }}
{% elif values.0 == similarToFormulation %} similar to Formulation: {{ values.1 }}
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

{% if values.0 == documents %} documents: {{ values.1 }}
{% elif values.0 == invents %} invents: {{ values.1 }}
{% elif values.0 == studies %} studies: {{ values.1 }}
{% elif values.0 == surveys %} surveys: {{ values.1 }}
{% elif values.0 == uses %} uses: {{ values.1 }}
{% endif %}
{% endfor %}
{% endfor %}

# Research Field

{% for values in ResearchField.values %}

## RF{{ forloop.counter }}: {{ values.Name }}

**Description**: {{ values.Description }}
**MathModDB**:{% if 'mathmoddb' in values.ID %} {{ values.ID|cut:"mathmoddb:" }} {% endif %} 
**WikiData**:{% if 'wikidata' in values.ID %} {{ values.ID|cut:"wikidata:" }} {% endif %}   
**MaRDI**:{% if 'mardi' in values.ID %} {{ values.ID|cut:"mardi:" }} {% endif %}

{% for relation in values.RelationRF1.values %}
{% if forloop.counter == 1 %}

&nbsp;

**Relations to other Research Fields**:

{% endif %}

{% if relation.0 == generalizedByField %} generalized by Field: {{relation.1 }} 
{% elif relation.0 == generalizesField %} generalizes Field: {{relation.1 }}
{% elif relation.0 == similarToField %} similar to Field: {{relation.1 }}
{% endif %}
{% endfor %} 

{% endfor %}

# Research Problem

{% for values in ResearchProblem.values %}

## RP{{ forloop.counter }}: {{ values.Name }}

**Description**: {{ values.Description }}
**MathModDB**:{% if 'mathmoddb' in values.ID %} {{ values.ID|cut:"mathmoddb:" }} {% endif %}
**WikiData**:{% if 'wikidata' in values.ID %} {{ values.ID|cut:"wikidata:" }} {% endif %} 
**MaRDI**:{% if 'mardi' in values.ID %} {{ values.ID|cut:"mardi:" }} {% endif %} 

{% for researchfield in values.RelationRF1.values %}
{% if forloop.counter == 1 %}

&nbsp;

**Relations to Research Fields**:

{% endif %}

contained in Field: {{ researchfield.1 }}
{% endfor %}

{% for relation in values.RelationRP1.values %}
{% if forloop.counter == 1 %}
&nbsp;

**Relations to other Research Problems**:

{% endif %}

{% if relation.0 == generalizedByProblem %} generalized by Problem: {{relation.1 }}
{% elif relation.0 == generalizesProblem %} generalizes Problem: {{relation.1 }}
{% elif relation.0 == similarToProblem %} similar to Problem: {{relation.1 }}
{% endif %}
{% endfor %}

{% endfor %}

# Quantity / Quantity Kind

{% for values in Quantity.values %}

## QQK{{ forloop.counter }}: {{ values.Name }}

**Description**: {{ values.Description }}
**Class**: {% if values.QorQK == Quantity %} Quantity {% elif values.QorQK == QuantityKind %} Quantity Kind {% endif %} 
**QUDT**:{% if 'qudt' in values.Reference %} {{ values.Reference|cut:"qudt:" }} {% endif %}
**MathModDB**:{% if values.MathModID and values.MathModID != 'not in MathModDB' %} {{ values.MathModID }} {% endif %}
**WikiData**:{% if 'wikidata' in values.ID %} {{ values.ID|cut:"wikidata:" }} {% endif %}
**MaRDI**:{% if 'mardi' in values.ID %} {{ values.ID|cut:"mardi:" }} {% endif %}
**Properties**: {% if values.Properties %} {% for value in values.Properties.values %} {% if value == isDimensionless %} Is Dimensionless {% elif value == isDimensional %} Is Dimensional {% elif value == isLinear %} Is Linear {% elif value == isNotLinear %} Is Not Linear {% endif %} {% if not forloop.last %}, {% endif %}{% endfor %} {% endif %}

{% if values.QorQK == Quantity %}

{% for values in values.RelationQQ.values %}
{% if forloop.counter == 1 %}
&nbsp;

**Relations to other Quantities**:

{% endif %}

{% if values.0 == generalizedByQuantity %} generalized by Quantity: {{ values.1 }}
{% elif values.0 == generalizesQuantity %} generalizes Quantity: {{ values.1 }}
{% elif values.0 == approximatedByQuantity %} approximated by Quantity: {{ values.1 }}
{% elif values.0 == approximatesQuantity %} approximates Quantity: {{ values.1 }}
{% elif values.0 == linearizedByQuantity %} linearized by Quantity: {{ values.1 }}
{% elif values.0 == linearizesQuantity %} linearizes Quantity: {{ values.1 }}
{% elif values.0 == nondimensionalizedByQuantity %} nondimensionalized by Quantity: {{ values.1 }}
{% elif values.0 == nondimensionalizesQuantity %} nondimensionalizes Quantity: {{ values.1 }}
{% elif values.0 == similarToQuantity %} similar to Quantity: {{ values.1 }}
{% endif %}
{% endfor %}

{% for values in values.RelationQQK.values %}
{% if forloop.counter == 1 %}
&nbsp;

**Relations to Quantity Kinds**:

{% endif %}

{% if values.0 == generalizedByQuantity %} generalized by Quantity Kind: {{ values.1 }}
{% elif values.0 == nondimensionalizedByQuantity %} nondimensionalized by Quantity Kind: {{ values.1 }}
{% elif values.0 == nondimensionalizesQuantity %} nondimensionalizes Quantity Kind: {{ values.1 }}
{% elif values.0 == similarToQuantity %} similar to Quantity Kind: {{ values.1 }}
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

**Properties**:{% for value in values.Properties.values %} {% if value == isConvex %} Is Convex {% elif value == isNotConvex %} Is Not Convex {% elif value == isDeterministic %} Is Deterministic {% elif value == isStochastic %} Is Stochastic {% elif value == isDimensionless %} Is Dimensionless {% elif value == isDimensional %} Is Dimensional {% elif value == isDynamic %} Is Dynamic {% elif value == isStatic %} Is Static {% elif value == isLinear %} Is Linear {% elif value == isNotLinear %} Is Not Linear {% elif value == isSpaceContinuous %} Is Space-Continuous {% elif value == isSpaceDiscrete %} Is Space-Discrete {% elif value == isSpaceIndependent %} Is Space-Independent {% elif value == isTimeContinuous %} Is Time-Continuous {% elif value == isTimeDiscrete %} Is Time-Discrete {% elif value == isTimeIndependent %} Is Time-Independent {% endif %} {% if not forloop.last %}, {% endif %} {% endfor %}

{% endif %}

{% elif values.QorQK == QuantityKind %}

{% for values in values.RelationQKQK.values %}
{% if forloop.counter == 1 %}
&nbsp;

**Relations to other Quantity Kinds**:

{% endif %}

{% if values.0 == nondimensionalizedByQuantity %} nondimensionalized by Quantity Kind: {{ values.1 }}
{% elif values.0 == nondimensionalizesQuantity %} nondimensionalizes Quantity Kind: {{ values.1 }}
{% elif values.0 == similarToQuantity %} similar to Quantity Kind: {{ values.1 }}
{% endif %}
{% endfor %}

{% for values in values.RelationQKQ.values %}
{% if forloop.counter == 1 %}
&nbsp;

**Relations to Quantities**:

{% endif %}

{% if values.0 == generalizesQuantity %} generalizes Quantity: {{ values.1 }}
{% elif values.0 == nondimensionalizedByQuantity %} nondimensionalized by Quantity: {{ values.1 }}
{% elif values.0 == nondimensionalizesQuantity %} nondimensionalizes Quantity: {{ values.1 }}
{% elif values.0 == similarToQuantity %} similar to Quantity: {{ values.1 }}
{% endif %}
{% endfor %}

{% endif %}
{% endfor %}
