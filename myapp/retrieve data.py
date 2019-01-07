import cloudant
from cloudant.client import Cloudant
from cloudant.error import CloudantException
from cloudant.result import Result, ResultByKey, QueryResult


serviceURL = "https://fe2e18ed-d0e4-4636-8a9d-1c154f97609f-bluemix:9cea356b0d2b461434c454fa379bf5fba7b48b99d90d072242dd7a2b61885f74@fe2e18ed-d0e4-4636-8a9d-1c154f97609f-bluemix.cloudant.com"
client = Cloudant("fe2e18ed-d0e4-4636-8a9d-1c154f97609f-bluemix","9cea356b0d2b461434c454fa379bf5fba7b48b99d90d072242dd7a2b61885f74", url="https://fe2e18ed-d0e4-4636-8a9d-1c154f97609f-bluemix:9cea356b0d2b461434c454fa379bf5fba7b48b99d90d072242dd7a2b61885f74@fe2e18ed-d0e4-4636-8a9d-1c154f97609f-bluemix.cloudant.com")
client.connect()

databaseName = "volunteer"

myDatabase = client.create_database(databaseName)
if myDatabase.exists():
   print("'{0}' successfully created.\n".format(databaseName))


#end_point = '{0}/{1}'.format(serviceURL, databaseName + "/_all_docs")
#params = {'include_docs': 'true'}

#response = client.r_session.get(end_point, params=params)
#print "{0}\n".format(response.json())


selector = {"selector": {"_id": {"$gt": "0"}},"fields": ["latField","lonField"],"sort": [{"_id": "asc"}]}

query = cloudant.query.Query(myDatabase, selector={'_id': {'$gt': 0}},fields=['latField', 'lonField', 'weightField', 'itemsField'])

for doc in query(limit=100)['docs']:
    print doc
