import logging
import azure.functions as func
import os
import json
from azure.cosmos import CosmosClient

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Counter function processed a request.')

    # Connection to Cosmos DB
    endpoint = os.environ["COSMOS_DB_ENDPOINT"]
    key = os.environ["COSMOS_DB_KEY"]
    client = CosmosClient(endpoint, key)

    database_name = "dbforvisitorssgouliotisgr"
    container_name = "Visitors"

    db = client.get_database_client(database_name)
    container = db.get_container_client(container_name)

    # Getting the counter file
    item_id = "counter"
    partition_key = item_id  # because /id is the partition key

    try:
        item = container.read_item(item=item_id, partition_key=partition_key)
        item["count"] += 1  # use "count" to match the current item
        container.replace_item(item=item, body=item)
    except:
        # If the item does not exist, create it
        item = {"id": "counter", "count": 1}
        container.create_item(body=item)

    return func.HttpResponse(
        json.dumps({"count": item["count"]}),
        mimetype="application/json"
    )
