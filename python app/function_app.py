import logging
import azure.functions as func
import os
import json
from azure.cosmos import CosmosClient

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Counter function processed a request.')

    #Connection to Cosmos DB
    endpoint = os.environ["https://dbsgouliotisgr.documents.azure.com:443/"]
    key = os.environ["AccountEndpoint=https://dbsgouliotisgr.documents.azure.com:443/;AccountKey=7rCz9x6O2ZVefjNH8R3a7vMi2bQ8z85TaBIm51QmR4nCMa1Mdl2Ybtrr88u8yhypDW9yVI7f5ATeACDbK4FcRw==;"]
    client = CosmosClient(endpoint, key)

    database_name = "dbforvisitorssgouliotisgr"
    container_name = "Visitors"

    db = client.get_database_client(database_name)
    container = db.get_container_client(container_name)

    # Getting the counter file
    item_id = "counter"
    partition_key = "counter"

    try:
        item = container.read_item(item=item_id, partition_key=partition_key)
        item["visits"] += 1
        container.replace_item(item=item, body=item)
    except:
        # If the item does not exist, create it
        item = {"id": "counter", "partitionKey": "counter", "visits": 1}
        container.create_item(body=item)

    return func.HttpResponse(
        json.dumps({"visits": item["visits"]}),
        mimetype="application/json"
    )
