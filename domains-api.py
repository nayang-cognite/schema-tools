#!/usr/bin/env python3

import os
from cognite.client import CogniteClient
from cognite.client.data_classes import TemplateGroup, TemplateGroup,TemplateGroupVersion
from cognite.client.data_classes import TemplateGroup,TemplateGroupVersion, TemplateInstance, ConstantResolver

def upsert_template_group(c):
    template_group_1 = TemplateGroup(
	    "test_template1",
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
    c.templates.versions.upsert("test_template1", template_group_version)
    res = c.templates.versions.list("test_template1", limit=10)    
    print(res)

def create_pump_instances(c):
    pump_1 = TemplateInstance(
        external_id="asset_1",
        template_name="Pump",
        field_resolvers={
            "inlet_pressure": ConstantResolver("timeseries_inletpressure_240"),
            "gen": ConstantResolver("Hex")
        }
    )
    pump_2 = TemplateInstance(
        external_id="asset_2",
        template_name="Pump",
        field_resolvers={
            "inlet_pressure": ConstantResolver("timeseries_inletpressure_249"),
	        "gen": ConstantResolver("hex")
	    }
	)
	
    template_group_list = c.templates.versions.list("nancy.pump.dashboard2")
    latest_version = template_group_list[0].version
    c.templates.instances.upsert("nancy.pump.dashboard2", latest_version, [pump_1, pump_2])

if __name__=="__main__":
    client_name = "schema-team-nancy"

    c = CogniteClient(client_name=client_name,
                      debug=False, 
                      base_url="http://localhost:8080", 
                      project=os.environ['COGNITE_PROJECT'], 
                      api_key=os.environ['COGNITE_API_KEY'])
    upsert_template_group(c)
    upsert_templatee_group_version(c)



