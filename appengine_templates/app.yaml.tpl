service: bts
runtime: python39

vpc_access_connector:
  name: projects/_PROJECT_ID/locations/europe-west2/connectors/vpcconnect

env_variables:
  BLAISE_API_URL: _BLAISE_API_URL
  BLAISE_SERVER_PARK: _BLAISE_SERVER_PARK
  TOTALMOBILE_USER: _TOTALMOBILE_USER
  TOTALMOBILE_PASSWORD_HASH: _TOTALMOBILE_PASSWORD_HASH

basic_scaling:
  idle_timeout: 10m
  max_instances: 10

handlers:
- url: /.*
  script: auto
  secure: always
  redirect_http_response_code: 301
