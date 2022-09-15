service: bts
runtime: python39

vpc_access_connector:
  name: projects/_PROJECT_ID/locations/europe-west2/connectors/vpcconnect

env_variables:
  BLAISE_API_URL: http://_BLAISE_API_URL
  BLAISE_SERVER_PARK: _BLAISE_SERVER_PARK
  TOTALMOBILE_INCOMING_USER: _TOTALMOBILE_INCOMING_USER
  TOTALMOBILE_INCOMING_PASSWORD_HASH: _TOTALMOBILE_INCOMING_PASSWORD_HASH

basic_scaling:
  idle_timeout: 10m
  max_instances: 10

handlers:
- url: /.*
  script: auto
  secure: always
  redirect_http_response_code: 301
