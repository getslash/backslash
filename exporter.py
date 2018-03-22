import json
from flask_app.utils.rendering import render_api_object
from flask_app.app import create_app
from flask_app import models
from flask_app.utils import statuses
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from sqlalchemy import desc, func
from sqlalchemy.orm import joinedload
import datetime

index_name = "test"
doc_type_name = "_doc"
es = Elasticsearch(['http://elastic:Password1@infra-elastic-search:9200'])
# res = es.get(index="test", doc_type='_doc', id=7350697)
# print(res['_source'])
app = create_app({'SQLALCHEMY_ECHO': False})
num_exceptions = 0
start_time_of_last_test = 0
exceptions = []
WINDOW_SIZE = 1000
start = 0
start_time_of_last_test = 1520849538.50607
with app.app_context():
    while True:
        documents = []
        stop = start + WINDOW_SIZE
        now = datetime.datetime.now()
        print("getting docs")

        tests = models.Test.query.filter(func.lower(models.Test.status)!= "planned").filter(func.lower(models.Test.status)!= "distributed").filter(models.Test.start_time <= start_time_of_last_test).order_by(desc(models.Test.start_time)).limit(1000).all()
        for test in tests:
            rendered_object = render_api_object(test)
            if test.parameters is not None:
                for param, param_value in rendered_object['parameters'].items():
                    rendered_object['parameters'][param] = str(param_value)
                rendered_object['parameters'].pop('dataset_binder_name.name', None)
                rendered_object['parameters'].pop('binder_name', None)
            if test.variation() is not None:
                for param, param_value in rendered_object['variation'].items():
                    rendered_object['variation'][param] = str(param_value)
                rendered_object['variation'].pop('dataset_binder_name.name', None)
                rendered_object['variation'].pop('binder_name', None)
            action = {
                "_index": index_name,
                "_type": doc_type_name,
                "_id": str(test.id),
                "_source": json.dumps(rendered_object)
            }
            documents.append(action)
            if len(documents) == WINDOW_SIZE:
                took = datetime.datetime.now() - now
                print(f"finished getting docs, time: {took}\n inserting to elastic")
                now = datetime.datetime.now()
                try:
                    success, _ = bulk(es, documents, index=index_name, raise_on_error=True)
                except Exception as e:
                    import ipdb; ipdb.set_trace()
                    num_exceptions += 1
                    exceptions.append(e)
                finally:
                    took = datetime.datetime.now() - now
                    start += WINDOW_SIZE
                    start_time_of_last_test = test.start_time
                    print(f"finished insert to elastic, time: {took}")
                    print(f"start_time_of_last_test: {start_time_of_last_test}")
                    print(f"status: {test.status}")
                    print(f"num_exceptions: {num_exceptions}")
                    documents = []
print(f"start_time_of_last_test: {start_time_of_last_test}")
pass
        #id_json = json.dumps({"index": {"_id": str(test.id)}})
            #test_json = json.dumps(render_api_object(test))
            #out_f.write(f"{id_json}\n{test_json}\n")

#1521120077.31678
#1520859062.9251
#1520777090.13323
