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

"""
Provides up to 3 offers randomly sorted
"""
from concurrent import futures
import random

import grpc

from offers_pb2 import (
    NftOffer,
    OfferResponse,
)
import offers_pb2_grpc

active_offers = [
    NftOffer(id=1, description="Buy 3 Nfts and get the 4th for free!"),
    NftOffer(id=2, description="Save 20% on your first purchase with coupon code NFTNEWBIE!"),
    NftOffer(id=3, description="Buy 7 NFTs and get 3 more for free!"),
    NftOffer(id=4, description="Subscribe to our newsletter and get the best deals directly in your inbox!"),
    NftOffer(id=5, description="Start selling your NFTs in our store and earn up to 30% more during the first year!"),
]

class OfferService(
    offers_pb2_grpc.OffersServicer
):
    def Offer(self, request, context):
        num_results = min(request.max_results, len(active_offers))
        random_offers = random.sample(
            active_offers, num_results
        )

        return OfferResponse(offers=random_offers)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    offers_pb2_grpc.add_OffersServicer_to_server(
        OfferService(), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()