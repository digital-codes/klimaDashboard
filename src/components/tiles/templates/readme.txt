this directory holds reusable templates. actual configuration is read from 
the directory ../<section>/<part>/<name>/ 
Make sure that card.json, lang.json and the generated text.json (from <lang>.md) 
are present at that location.

dynamic imports need a specific construction, in particular each dir level must be indicated explicitly

make sure views load the template with section,part and name props set properly

