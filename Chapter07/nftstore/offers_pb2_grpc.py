# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import offers_pb2 as offers__pb2


class OffersStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Offer = channel.unary_unary(
                '/Offers/Offer',
                request_serializer=offers__pb2.OfferRequest.SerializeToString,
                response_deserializer=offers__pb2.OfferResponse.FromString,
                )


class OffersServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Offer(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_OffersServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Offer': grpc.unary_unary_rpc_method_handler(
                    servicer.Offer,
                    request_deserializer=offers__pb2.OfferRequest.FromString,
                    response_serializer=offers__pb2.OfferResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Offers', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Offers(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Offer(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Offers/Offer',
            offers__pb2.OfferRequest.SerializeToString,
            offers__pb2.OfferResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
