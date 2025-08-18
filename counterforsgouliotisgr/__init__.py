import logging
import azure.functions as func
import os
import json
from azure.cosmos import CosmosClient, exceptions

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Counter function processed a request.')

    # Connection to Cosmos DB with endpoint & key from environment variables
    endpoint = os.environ["COSMOS_DB_ENDPOINT"]  
    key = os.environ["COSMOS_DB_KEY"]          

    client = CosmosClient(endpoint, key)

    database_name = "dbforvisitorssgouliotisgr"
    container_name = "Visitors"

    db = client.get_database_client(database_name)
    container = db.get_container_client(container_name)

    # Item for counting visits
    item_id = "counter"
    partition_key = "counter"

    try:
        item = container.read_item(item=item_id, partition_key=partition_key)
        item["count"] += 1
        container.replace_item(item=item, body=item)
    except exceptions.CosmosResourceNotFoundError:
        # If the item does not exist, create it
        item = {"id": "counter", "count": 1, "partitionKey": "counter"}
        container.create_item(body=item)

    return func.HttpResponse(
        json.dumps({"visits": item["count"]}),
        mimetype="application/json"
    )
