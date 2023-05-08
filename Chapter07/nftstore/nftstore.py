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

import os

from flask import Flask, render_template
import grpc

from catalog_pb2 import CatalogRequest
from catalog_pb2_grpc import CatalogStub

from offers_pb2 import OfferRequest
from offers_pb2_grpc import OffersStub

app = Flask(__name__)

catalog_host = os.getenv("CATALOG_HOST", "localhost")
catalog_channel = grpc.insecure_channel(
    f"{catalog_host}:50052"
)
catalog_client = CatalogStub(catalog_channel)

offers_host = os.getenv("OFFERS_HOST", "localhost")
offers_channel = grpc.insecure_channel(
    f"{offers_host}:50051"
)
offers_client = OffersStub(offers_channel)

@app.route("/")
def render_homepage():
    catalog_request = CatalogRequest(
        max_results=12, product_id = "dummy"
    )
    catalog_response = catalog_client.Catalog(
        catalog_request
    )
    offers_request = OfferRequest(
        max_results=1
    )
    offers_response = offers_client.Offer(
        offers_request
    )
    return render_template(
        "homepage.html",
        items=catalog_response.items,
        offer=offers_response.offers[0],
    )

@app.route("/product/<product_id>")
def show_product_info(product_id):
    print("Loading info for product ID {}".format(product_id))
    catalog_request = CatalogRequest(
        max_results=1, product_id=product_id
    )
    catalog_response = catalog_client.Catalog(
        catalog_request
    )
    offers_request = OfferRequest(
        max_results=1
    )
    offers_response = offers_client.Offer(
        offers_request
    )

    return render_template(
        "product_info.html",
        item=catalog_response.items[0],
        offer=offers_response.offers[0],
    )

if __name__ == '__main__':
    app.run()