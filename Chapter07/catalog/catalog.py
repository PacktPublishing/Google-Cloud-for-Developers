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
Provides the specified number of items from the product catalog
"""
from concurrent import futures
import grpc
import os
import random
import time

from catalog_pb2 import (
    CatalogItem,
    CatalogResponse,
)
import catalog_pb2_grpc

product_catalog = [
    CatalogItem(id="electric-sheep01", title="Sheeps'R Us", author="Stephan Doe", description="Stephan's psychodelic color palette takes NFTs to the next level.", rating=3, price_dollars="5", price_cents="00"),
    CatalogItem(id="electric-sheep02", title="Colourful Nightmare", author="Jane Smith", description="Simple but impactful, this masterpiece is worth every single cent.", rating=5, price_dollars="7", price_cents="75"),
    CatalogItem(id="electric-sheep03", title="Eat that sheep!", author="AuroraNFT", description="AuroraNFT is back with incredible colors in his second year with us!", rating=2, price_dollars="22", price_cents="00"),
    CatalogItem(id="electric-sheep04", title="Sh33p 1.3", author="Julian Fake", description="Challenging piece of art whose eyes are always watching!", rating=1, price_dollars="34", price_cents="50"),
    CatalogItem(id="electric-sheep05", title="Count them if you dare!", author="Mike O'Phone", description="Another psychodelic work inviting us to try counting the sheep. Can you?", rating=4, price_dollars="7", price_cents="00"),
    CatalogItem(id="electric-sheep06", title="My dear NFT sheep", author="Evo Celatti", description="Evo offers us this crazy logo that you shouldn't miss.", rating=3, price_dollars="4", price_cents="00"),
    CatalogItem(id="electric-sheep07", title="Electrosheep", author="AuroraNFT", description="Monochrome NFT that will look great as your wallpaper, too.", rating=5, price_dollars="2", price_cents="99"),
    CatalogItem(id="electric-sheep08", title="Beep the Sheep", author="Mike O'Phone", description="Synthetic art at its maximum exponent.", rating=2, price_dollars="1", price_cents="25"),
    CatalogItem(id="electric-sheep09", title="Sheepotronic", author="Jane Smith", description="Funny and happy NFT that will make you smile for sure!", rating=1,price_dollars="15", price_cents="00"),
    CatalogItem(id="electric-sheep10", title="Counting NFT sheeps", author="Evo Celatti", description="Evo is back with this dark and disturbing work.", rating=4,price_dollars="3", price_cents="15"),
    CatalogItem(id="electric-sheep11", title="Decrypt da flock", author="Stephan Doe", description="Will you be able to understand the message? We are still trying...", rating=3,price_dollars="8", price_cents="00"),
    CatalogItem(id="electric-sheep12", title="Electroflock", author="Julian Fake", description="The floating sheep can help you in your mindfulness sessions", rating=1,price_dollars="9", price_cents="50"),
]

class CatalogService(
    catalog_pb2_grpc.CatalogServicer
):
    def Catalog(self, request, context):
        latency = int(os.getenv("EXTRA_LATENCY", "0"))
        if latency>0:
            time.sleep(latency)
        num_results = min(request.max_results, len(product_catalog))
        random_items = []
        if request.product_id != "dummy":
            for item in product_catalog:
                if item.id == request.product_id:
                    random_items.append(item)
        else:
            random_items = random.sample(
                product_catalog, num_results
            )

        return CatalogResponse(items=random_items)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    catalog_pb2_grpc.add_CatalogServicer_to_server(
        CatalogService(), server
    )
    server.add_insecure_port("[::]:50052")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()