import logging
from concurrent import futures

import grpc
from cloudx_connector_pb2_grpc import CloudxConnectorServicer, add_CloudxConnectorServicer_to_server
from cloudx_connector_pb2 import ComponentResponse
import aws_client


class AWSServicer(CloudxConnectorServicer):
    def ShowComponents(self, request, context):
        resources = aws_client.read_all_resources();
        for res in resources:
            yield ComponentResponse(type=res['resourceType'], id=res['resourceId'], name= res['resourceName'] if 'resourceName' in res else '')


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_CloudxConnectorServicer_to_server(AWSServicer(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
