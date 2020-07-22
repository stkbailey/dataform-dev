import json
import pathlib
import dataclasses
import yaml

from typing import List, Dict

@dataclasses.dataclass
class DataSourceSpec:
    id: str
    name: str
    schema: str
    sql_name: str
    description: str = None
    documentation: str = None
    tags: List[str] = dataclasses.field(default_factory=list)
    columns: Dict = dataclasses.field(default_factory=dict)


class DataformParser:

    def __init__(self, file_path):
        self._plan = self.read_compiled_plan(file_path)
        self.data_sources = self.map_targets_to_data_sources()


    def read_compiled_plan(self, file_path):
        txt = pathlib.Path(file_path).read_text()
        return json.loads(txt)


    def map_targets_to_data_sources(self):
        targets = self._plan["targets"]
        data_sources = []
        for target in targets:
            node, category = self.find_target_node(target)
            if category == "tables":
                ds = self.map_table_to_data_source(node)
            elif category == "declarations":
                ds = self.map_declaration_to_data_source(node)
            data_sources.append({ds.id: dataclasses.asdict(ds)})
        return data_sources


    def find_target_node(self, target):
        for category in ["tables", "declarations"]:
            resource_list = self._plan[category]
            for node in resource_list:
                if node["canonicalTarget"] == target:
                    return node, category


    def map_table_to_data_source(self, node):
        ds = DataSourceSpec(
            id = node["name"],
            name = node["name"],
            schema = node["target"]["schema"],
            sql_name = node["target"]["name"],
            description = "Created by Dataform.",
            documentation = node.get("actionDescriptor", {}).get("description"),
            tags = node.get("tags"),
            columns = node.get("actionDescriptor", {}).get("columns")
        )
        return ds

    def map_declaration_to_data_source(self, node):
        ds = DataSourceSpec(
            id = node["name"],
            name = node["name"],
            schema = node["target"]["schema"],
            sql_name = node["target"]["name"],
            description = "Created by Dataform.",
            documentation = node.get("actionDescriptor", {}).get("description"),
            tags = node.get("tags"),
            columns = node.get("actionDescriptor", {}).get("columns")
        )
        return ds

    def dump_yaml(self):
        txt = yaml.dump(self.data_sources)
        print(txt)



if __name__ == "__main__":
    fp = "./compiled.json"
    dfp = DataformParser(fp)
    print(dfp.dump_yaml())





"""
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
"""