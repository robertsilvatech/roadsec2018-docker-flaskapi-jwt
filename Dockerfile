FROM alpine


COPY requirements.txt /requirements.txt
RUN apk add --no-cache python3 && pip3 install -r /requirements.txt
RUN mkdir -p /app
WORKDIR /app



#docker container run --name roadsecapi -v /Users/robertsilva/Documents/MyWorkspace/Repo/github.org/py013/roadsec2018/:/app -p 8091:5000 --rm -it 00de4bf8967a