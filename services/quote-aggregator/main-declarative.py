import json
import time
import grpc
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
import logging
import os
from dapr.clients import DaprClient
from dapr.clients.grpc._response import TopicEventResponse
from model.cloud_events import CloudEvent

statestore_component = os.getenv('QUOTE_AGGREGATE_TABLE', 'kvstore')
pubsub_component = os.getenv('PUBSUB_COMPONENT', 'pubsub')
topic_name = os.getenv('TOPIC_NAME', 'quotes')

logging.basicConfig(level=logging.INFO)

# region Declarative subscription
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello, World!"}

@app.post('/loan-quotes')
def loan_quotes(event: CloudEvent):
    with DaprClient() as d:
        try:

            logging.info(f"Event contained aggregated quote with details: {event.data}")

            quote_aggregate = json.loads(event.data["quote_aggregate"])

            # save aggregate data
            d.save_state(store_name=statestore_component,
                         key=quote_aggregate["request_id"],
                         value=json.dumps(quote_aggregate),
                         state_metadata={"contentType": "application/json"})
            
            logging.info(f"Quote successfully saved to db {statestore_component}")

            return TopicEventResponse('success')

        except grpc.RpcError as err:
            logging.info(f"Error={err}")
            raise HTTPException(status_code=500, detail=err.details())
# endregion

if __name__ == "__main__":
    uvicorn.run(app, port=5002)