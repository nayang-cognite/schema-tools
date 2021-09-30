#!/usr/bin/env python3

import os
from cognite.client import CogniteClient
from cognite.client.data_classes import TemplateGroup, TemplateGroup,TemplateGroupVersion
from cognite.client.data_classes import TemplateGroup,TemplateGroupVersion, TemplateInstance, ConstantResolver

TEMPLATE_GROUP="test_template1"
TEMPLATE_INSTANCE="instance_1"

def upsert_template_group(c):
    template_group_1 = TemplateGroup(
	    TEMPLATE_GROUP,
	    "test"
	)
    c.templates.groups.upsert(template_group_1)
    res = c.templates.groups.list(limit=10)
    print(res)

def upsert_templatee_group_version(c):
    schema = '''
        type Generic @template {
            name: String
        }
    '''
    template_group_version = TemplateGroupVersion(schema)
    try:
        c.templates.versions.upsert(TEMPLATE_GROUP, template_group_version)
        res = c.templates.versions.list(TEMPLATE_GROUP, limit=10)    
        print(res)
    except Exception as e:
        print("@@@ exception")
        print("\t %s" % e)

def upsert_instance(c, instance_external_id):
    instance = TemplateInstance(
        external_id=instance_external_id,
        template_name="Generic",
        field_resolvers={
            "name": ConstantResolver("max2")
        }
    )
    template_group_list = c.templates.versions.list(TEMPLATE_GROUP)
    latest_version = template_group_list[0].version
    print("@@@ Latest version created on %s is %d" % (TEMPLATE_GROUP, latest_version))
    try:
        c.templates.instances.upsert(TEMPLATE_GROUP, latest_version, [instance])
    except Exception as e:
        print("@@@ exception")
        print("\t %s" % e)

def run_graphql(c):
    query = '''
{
    genericQuery {
        items {
            _externalId
            name 
        }
    }
}
'''
    result = c.templates.graphql_query(TEMPLATE_GROUP, 1, query)
    print(result)

if __name__=="__main__":
    client_name = "schema-team-nancy"
    c = CogniteClient(client_name=client_name,
                      debug=False, 
                      base_url="http://localhost:8080", 
                      project=os.environ['COGNITE_PROJECT'], 
                      api_key=os.environ['COGNITE_API_KEY'])
    upsert_template_group(c)
    upsert_templatee_group_version(c)
    upsert_instance(c, "instance_2")
    run_graphql(c)
