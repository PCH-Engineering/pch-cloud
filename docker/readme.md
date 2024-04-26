# Docker 
pch-cloud docker image can be pulled from public.ecr.aws/pch-engineering/1067/edgebackend

| Target     | path                                                  | 
| ---------- | ----------------------------------------------------- |
| x86_64     | public.ecr.aws/pch-engineering/1067/edgebackend       |
| arm64      | public.ecr.aws/pch-engineering/1067/edgebackend_arm64 |

## Docker run 
docker run -e ASPNETCORE_URLS='http://0.0.0.0:5000' -p 5000:5000 public.ecr.aws/pch-engineering/1067/edgebackend

## Docker compose
Use the docker-compose.yml 

### Start (running detached)

`docker-compose up -d`

or (newer docker installations includes docker-compose)

`docker compose up -d`

### Stop 
`docker-compose down`
or 
`docker compose down`

### Usefull environment variables
| KEY         | Description | Default | 
| ----------- | ----------- | ------- | 
| ASPNETCORE_URLS | Internal listen port | http://0.0.0.0:5000 | 







