import json
import pathlib




def read_compiled_plan(file_path):
    txt = pathlib.Path(file_path).read_text()
    return json.loads(txt)

fp = "./compiled.json"
f = read_compiled_plan(fp)


tables = f["tables"]

sources = "declarations"



tables
keys:
- name (dataform.clockify_projects)
- dependencies (dev.clockify.projects)
- type: table/view
- target: (schema: dataform, clockify_projects)
- query
- disabled = False
- tags: a, b
- actionDescriptor:
    - description: txt
    - columns:
        - path: [id]
          description
        - path: clientid
          description
          tags
        - path: name
          tags
- dependencyTargets:
    - {scchema: , name: , database: }
- canonicalTarget:
    schema: 
    name: 
        

declarations:
{'name': 'dev.clockify.projects',
  'target': {'schema': 'clockify', 'name': 'projects', 'database': 'dev'},
  'fileName': 'definitions/sources/projects.sqlx',
  'canonicalTarget': {'schema': 'clockify',
   'name': 'projects',
   'database': 'dev'}