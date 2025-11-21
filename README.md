**Getting started**

    #qdrant server open
    docker run -p 6336:6336 -v $(pwd)/qdrant_data:qdrant/storage qdrant/qdrant

    #docker image file make
    docker build -t healing-recipe .

    #docker container execute
    docker run -p 8000:8000 healing-recipe