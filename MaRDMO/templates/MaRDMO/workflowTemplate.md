# {{ title }}

{% if Publication.Exists.1 %}
PID (if applicable): doi:[{{ Publication.Exists.1|cut:"doi:" }}](https://doi.org/{{ Publication.Exists.1|cut:"doi:" }})
{% else %}
PID (if applicable): no related publication
{% endif %}

## Problem Statement

{{ GeneralInformation.ProblemStatement }}    

### Object of Research and Objective

{{ GeneralInformation.ResearchObjective }}    

### Procedure

{{ GeneralInformation.Procedure }}    

### Involved Disciplines
    
**Mathematical Areas:**

{% for value in MathematicalArea.values %} {% if value.mardiId != 'tbd' %} {{ forloop.counter }} - [{{ value.Name }}]({{ value.uri }}) {% endif %} {% if value.mardiId == 'tbd' %} {{ forloop.counter }} - {{ value.Name }} {% endif %} 
{% endfor %}

**Non-Mathematical Disciplines:**

{% for value in NonMathematicalDiscipline.values %} {% if value.mardiId != 'tbd' %} {{ forloop.counter }} - [{{ value.Name }}]({{ value.uri }}) {% endif %} {% if value.mardiId == 'tbd' %} {{ forloop.counter }} - {{ value.Name }} {% endif %}
{% endfor %}

### Data Streams
        
{% for value in GeneralInformation.DataStream.values %} {{ forloop.counter }} - {{ value }}
{% endfor %}    

## Model
        
{% for value in Model.values %} {% if value.mardiId != 'tbd' %} [{{ value.Name }}]({{ value.uri }}) ({{ value.Description }}) {% elif value.mardiId == 'tbd' %} {{ value.Name }}  ({{ value.Description}}) {% endif %}
{% endfor %}

### Discretization

{% for value in Model.values %} {% if TimeDiscrete in value.Properties.values %} * Time: Yes {% else %} * Time: No {% endif %} 
{% if SpaceDiscrete in value.Properties.values %} * Space: Yes {% else %} * Space: No {% endif %}
{% endfor %}

### Variables

| Name | Unit | Symbol| dependent/independent |
|------|------|-------|-----------------------|
{% for values in Task.values %} {% for value in values.values %} {% if value.Property == TaskInput or value.Property == TaskOutput %} | {{ value.Quantity }} | | {{ value.Symbol }} | {% if TaskInput == value.Property %} independent {% elif TaskOutput == value.Property %} dependent {% endif %} | {% endif %} 
{% endfor %} {% endfor %}

### Parameters

| Name | Unit | Symbol|
|------|------|-------|
{% for values in Task.values %} {% for value in values.values %} {% if value.Property == TaskParameter %} | {{value.Quantity }} | | {{ value.Symbol }} | {% endif %}
{% endfor %} {% endfor %}

## Process Information

### Process Steps

| Name | Description | Input | Output | Method | Parameter | Environment | Mathematical Area |
|------|-------------|-------|--------|--------|-----------|-------------|-------------------|
{% for values in ProcessStep.values %} | {{ values.Name }} | {{ values.Description }} | {% for input in values.Input.values %} {{ input }} {% if not forloop.last %}, {% endif %} {% endfor %} | {% for output in values.Output.values %} {{ output }} {% if not forloop.last %}, {% endif %} {% endfor %} | {% for method in values.Method.values %} {{ method }} {% if not forloop.last %}, {% endif %} {% endfor %} | {{ values.Parameter }} | {% for environment in values.Environment.values %} {{ environment }} {% if not forloop.last %}, {% endif %} {% endfor %} | {% for matharea in values.MathArea.values %} {{ matharea }} {% if not forloop.last %}, {% endif %} {% endfor %} |
{% endfor %}

### Applied Methods

| ID | Name | Process Step | Parameter | implemented by |
|----|------|--------------|-----------|----------------|
{% for values in Method.values %} | {% if values.mardiId != 'tbd' %} mardi:[{{ values.mardiId }}]({{ values.uri }}) {% elif values.mardiId == 'tbd' %} mardi:{{ values.mardiId }} {% endif %} | {{ values.Name }} | {% for processstep in values.ProcessStep.values %} {{ processstep }} {% if not forloop.last %}, {% endif %} {% endfor %} | {{ values.Parameter }} | {% for software in values.Software.values %} {{ software }} {% if not forloop.last %}, {% endif %} {% endfor %} |
{% endfor %}

### Software used

| ID | Name | Description | Version | Programming Language | Dependencies | versioned | published | documented |
|----|------|-------------|---------|----------------------|--------------|-----------|-----------|------------|
{% for values in Software.values %} | {% if values.mardiId != 'tbd' %} mardi:[{{ values.mardiId }}]({{ values.uri }}) {% elif values.mardiId == 'tbd' %} mardi:{{ values.mardiId }} {% endif %} | {{ values.Name }} | {{ values.Description }} | {{ values.Version }} | {% for subproperty in values.SubProperty.values %} {% if subproperty.mardiId != 'tbd' %} [{{ subproperty.Name }}]({{ subproperty.uri }}) {% elif subproperty.mardiId == 'tbd' %} {{ subproperty.Name }} {% endif %} {% if not forloop.last %}, {% endif %} {% endfor %} | {% for dependency in values.Dependency.values %} {{ dependency }} {% if not forloop.last %}, {% endif %} {% endfor %} | {% if values.Versioned.0 == YesText %} [Yes]({{values.Versioned.1}}) {% elif values.Versioned.0 != YesText %} No {% endif %} | {% if values.Published.0 == YesText %} [Yes]({{values.Published.1}}) {% elif values.Published.0 != YesText %} No {% endif %} | {% if values.Documented.0 == YesText %} [Yes]({{values.Documented.1}}) {% elif values.Documented.0 != YesText %} No {% endif %} |
{% endfor %}

{% if Settings.WorkflowType == Computation %}  
### Hardware

| ID | Name | Processor | Compiler | #Nodes | #Cores |
|----|------|-----------|----------|--------|--------|
{% for values in Hardware.values %} | {{ values.ID }} | {{ values.Name }} | {{ values.Processor }} | {{ values.Compiler }} | {{ values.Node }} | {{ values.Core }} |
{% endfor %}
{% endif %}

{% if Settings.WorkflowType == Analysis %}
### Experimental Devices

| ID | Name | Description | Version | Part Number | Serial Number | Location | Software|
|----|------|-------------|---------|-------------|---------------|----------|---------|
{% for values in ExperimentalDevice.values %} | {{ values.ID }} | {{ values.Name }} | {{ values.Description }} | {{ values.Version }} | {{ values.PartNumber }} | {{ values.SerialNumber }} | {{ values.Location }} | {{ values.Software }} |
{% endfor %}
{% endif %}

### Input Data

| ID | Name | Size | Data Structure | Format Representation | Format Exchange | binary/text | proprietary | to publish | to archive |
|----|------|------|----------------|-----------------------|-----------------|-------------|-------------|------------|------------|
{% for values in DataSet.values %} {% if 'Input' in values.Type.values %} | {% if values.mardiId != 'tbd' %} mardi:[{{ values.mardiId }}]({{ values.uri }}) {% elif values.mardiId == 'tbd' %} mardi:{{ values.mardiId }} {% endif %} | {{ values.Name }} | {% if values.Size == Small %} Small (KB - MB) {% elif values.Size == Medium %} Medium (MB - GB) {% elif values.Size == Large %} Large (GB - TB) {% elif value.Size == VeryLarge %} Very Large (>TB) {% endif %} | {{ values.DataStructure }} | {{ values.RepresentationFormat }} | {{ values.ExchangeFormat }} | {% if values.BinaryText == Binary %} Binary {% elif values.BinaryText == Text %} Text {% endif %} | {% if values.Proprietary == Yes %} Yes {% elif values.Proprietary == No %} No {% endif %} | {% if values.Publication == Yes %} Yes {% elif values.Publication == No %} No {% endif %} | {% if values.Archiving.0 == YesText %} {{ values.Archiving.1 }} {% elif values.Archiving.0 == NoText %} No {% endif %} | {% endif %}
{% endfor %}

### Output Data

| ID | Name | Size | Data Structure | Format Representation | Format Exchange | binary/text | proprietary | to publish | to archive |
|----|------|------|----------------|-----------------------|-----------------|-------------|-------------|------------|------------|
{% for values in DataSet.values %} {% if 'Output' in values.Type.values %} | {% if values.mardiId != 'tbd' %} mardi:[{{ values.mardiId }}]({{ values.uri }}) {% elif values.mardiId == 'tbd' %} mardi:{{ values.mardiId }} {% endif %} | {{ values.Name }} | {% if values.Size == Small %} Small (KB - MB) {% elif values.Size == Medium %} Medium (MB - GB) {% elif values.Size == Large %} Large (GB - TB) {% elif value.Size == VeryLarge %} Very Large (>TB) {% endif %} | {{ values.DataStructure }} | {{ values.RepresentationFormat }} | {{ values.ExchangeFormat }} | {% if values.BinaryText == Binary %} Binary {% elif values.BinaryText == Text %} Text {% endif %} | {% if values.Proprietary == Yes %} Yes {% elif values.Proprietary == No %} No {% endif %} | {% if values.Publication == Yes %} Yes {% elif values.Publication == No %} No {% endif %} | {% if values.Archiving.0 == YesText %} {{ values.Archiving.1 }} {% elif values.Archiving.0 == NoText %} No {% endif %} | {% endif %}
{% endfor %}
                                                           
## Reproducibility

{% if Settings.WorkflowType == Computation %}
### Mathematical Reproducibility
{% if ReproducibilityComputational.Mathematically.0 == YesText %}
Yes: {{ ReproducibilityComputational.Mathematically.1 }}
{% elif ReproducibilityComputational.Mathematically.0 == NoText %}
No
{% endif %}
### Runtime Reproducibility
{% if ReproducibilityComputational.Runtime.0 == YesText %}
Yes: {{ ReproducibilityComputational.Runtime.1 }}
{% elif ReproducibilityComputational.Runtime.0 == NoText %}
No
{% endif %}
### Reproducibility of Results
{% if ReproducibilityComputational.Result.0 == YesText %}
Yes: {{ ReproducibilityComputational.Result.1 }}
{% elif ReproducibilityComputational.Result.0 == NoText %}
No
{% endif %}
### Reproducibility on original Hardware
{% if ReproducibilityComputational.OriginalHardware.0 == YesText %}
Yes: {{ ReproducibilityComputational.OriginalHardware.1 }}
{% elif ReproducibilityComputational.OriginalHardware.0 == NoText %}
No
{% endif %}
###Reproducibility on other Hardware
{% if ReproducibilityComputational.OtherHardware.0 == YesText %}
Yes: {{ ReproducibilityComputational.OtherHardware.1 }}
{% elif ReproducibilityComputational.OtherHardware.0 == NoText %}
No
{% endif %}
### Transferability to
{% for value in ReproducibilityComputational.Transferability.values %}
{{ value }}
{% if not forloop.last %}<br>{% endif %}
{% endfor %}
{% endif %}

{% if Settings.WorkflowType == Analysis %}
### Reproducibility on original Device/Instrument/Hardware
{% if ReproducibilityAnalysis.OriginalDevice.0 == YesText %}
Yes: {{ ReproducibilityAnalysis.OriginalDevice.1 }}
{% elif ReproducibilityAnalysis.OriginalDevice.0 == NoText %}
No
{% endif %}
### Reproducibility on other Device/Instrument/Hardware
{% if ReproducibilityAnalysis.OtherDevice.0 == YesText %}
Yes: {{ ReproducibilityAnalysis.OtherDevice.1 }}
{% elif ReproducibilityAnalysis.OtherDevice.0 == NoText %}
No
{% endif %}
### Transferability to
{% for value in ReproducibilityAnalysis.Transferability.values %}
{{ value }}
{% endfor %}
{% endif %}

## Legend
The following abbreviations are used in the document to indicate/resolve IDs:
doi: DOI / https://dx.doi.org/
sw: swMATH / https://swmath.org/software/
wikidata: https://www.wikidata.org/wiki/
mardi: https://portal.mardi4nfdi.de/wiki/

