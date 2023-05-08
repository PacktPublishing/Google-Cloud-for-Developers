# Building the containers for Chapter 7

While you can use the prebuilt containers that I referenced in the exercise, here are the instructions to build your own containers in Cloud Shell, just in case you may want to try it.

Otherwise, just follow the instructions in the chapter to deploy the sample application in your favourite public cloud provider.

First of all, let's create a virtual environment and activate it:

```
python3 -m venv venv
source venv/bin/activate
```

Next, let's clone this repository and get to the code for chapter 7:

```
git clone https://github.com/PacktPublishing/Google-Cloud-for-Developers
cd Google-Cloud-for-Developers/Chapter07
```

Then, let's build the protobuffers for each of the components:

First, let's go for the offers module. Notice that I included a pre-compiled version of the protobuffer files, that you can optionally overwrite using the last command below:
```
cd offers

python -m pip install -r requirements.txt 

python -m grpc_tools.protoc -I ../protobufs --python_out=. \
  --grpc_python_out=. ../protobufs/offers.proto
```

You can run this module in the background using the following command to check if it's working as expected. Notice that you will not see any output until you launch the main store module, which interacts with this one:

```
python offers.py &
```

Then, let's do the same for the catalog module. Notice that I included a pre-compiled version of the protobuffer files, that you can optionally overwrite using the last command below:

```
cd ../catalog

python -m pip install -r requirements.txt 

python -m grpc_tools.protoc -I ../protobufs --python_out=.  \
  --grpc_python_out=. ../protobufs/catalog.proto
```

You can run this module in the background using the following command to check if it's working as expected. Notice that you will not see any output until you launch the main store module, which interacts with this one:

```
python catalog.py &
```

Last, it's time to compile and generate the required files for the main module, named `nftstore`. The main module has more commands to run because it uses the protobuffers of the other two modules. Notice that I included a pre-compiled version of the protobuffer files, that you can optionally overwrite using the last two commands below:

```
cd ../nftstore

python -m pip install -r requirements.txt 

python -m grpc_tools.protoc -I ../protobufs --python_out=.  \
  --grpc_python_out=. ../protobufs/catalog.proto

python -m grpc_tools.protoc -I ../protobufs --python_out=. \
  --grpc_python_out=. ../protobufs/offers.proto

```

If you want to try the main module on the command line, you can use the following command:
```
FLASK_APP=nftstore.py flask run
```

If you get an error when trying to launch flask, with a message similar to `ImportError: cannot import name 'soft_unicode' from 'markupsafe'`, just downgrade markupsafe using the following command and then try again:

```
python -m pip install markupsafe==2.0.1
FLASK_APP=nftstore.py flask run
```

Once you launch the main module, you will be able to test the web app by running `curl http://127.0.0.1:5000/` from another tab of your Cloud Shell.

After testing all the components, press `Control + C` to exit, then use the sequence of `fg` and `Control + C` two more times to bring the other two processes to the background and kill them.

Once all the processes have been killed, it's time to build each of the containers from the main chapter directory (Chapter07). Notice that each of the docker build commands will take a few seconds to complete:

```
cd ..
docker build . -f offers/Dockerfile -t offers
docker build . -f catalog/Dockerfile -t catalog
docker build . -f nftstore/Dockerfile -t nftstore
docker build . -f load_generator/Dockerfile -t load_generator
```

If we want to try the containers locally, we should first create a local demo network:
```
docker network create microservices-demo
```

And then we can run each of them by configuring them to listen on a different port of our loopback interface. Run each of the following commands in a different tab of your Cloud Shell and use a fourth tab to run `curl` and validate the output:

```
docker run -p 127.0.0.1:50051:50051/tcp --network microservices-demo \
  --name offersv1 offers
docker run -p 127.0.0.1:50052:50052/tcp --network microservices-demo \
  --name catalogv1 catalog
docker run -p 127.0.0.1:5000:5000/tcp --network microservices-demo \
  -e OFFERS_HOST=offersv1 -e CATALOG_HOST=catalogv1 --name nftstorev1 nftstore
curl http://127.0.0.1:5000/
```

And the final step wpuld be to tag each of the generated containers as the latest version in our repository and then we can just push them to our repository. Please remember to replace `<REPOSITORY_NAME>` with the name of a docker repository that you should [create in advance](https://docs.docker.com/docker-hub/repos/):

```
docker tag offers:latest <REPOSITORY_NAME>/offers:latest
docker push <REPOSITORY_NAME>/offers:latest

docker tag catalog:latest <REPOSITORY_NAME>/catalog:latest
docker push <REPOSITORY_NAME>/catalog:latest

docker tag nftstore:latest <REPOSITORY_NAME>/nftstore:latest
docker push <REPOSITORY_NAME>/nftstore:latest

docker tag load_generator:latest <REPOSITORY_NAME>/load_generator:latest
docker push <REPOSITORY_NAME>/load_generator:latest
```

Please remember that if you decide to use your own repository and containers, you should update the reference in the exercise files. Just replace all instances of `hectorparra` in `yaml/kubernetes.yaml` and `yaml/catalog-v2.yaml` with your own full repository name.
