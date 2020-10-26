import logging

import grpc

from aws_connector.cloudx_connector_pb2_grpc import CloudxConnectorStub
from aws_connector.cloudx_connector_pb2 import PlatformRequest


def run():
    with grpc.insecure_channel('localhost:50052') as channel:
        client = CloudxConnectorStub(channel)
        print("-------------- Show Resources --------------")
        request = PlatformRequest(clintId="1234")
        resources = client.ShowComponents(request)
        for res in resources:
            print("%s %s %s" % (res.type, res.id, res.name))
        print("-------------- End Resources --------------")


if __name__ == '__main__':
    logging.basicConfig()
    run()
