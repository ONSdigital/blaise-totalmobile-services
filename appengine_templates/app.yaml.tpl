service: bts
runtime: python313

vpc_access_connector:
  name: _VPC_CONNECTOR

env_variables:
  BLAISE_API_URL: http://_BLAISE_API_URL
  BLAISE_SERVER_PARK: _BLAISE_SERVER_PARK
  CMA_SERVER_PARK: _CMA_SERVER_PARK
  TOTALMOBILE_INCOMING_USER: _TOTALMOBILE_INCOMING_USER
  TOTALMOBILE_INCOMING_PASSWORD_HASH: _TOTALMOBILE_INCOMING_PASSWORD_HASH

automatic_scaling:
  min_instances: _MIN_INSTANCES
  max_instances: _MAX_INSTANCES
  target_cpu_utilization: _TARGET_CPU_UTILIZATION

handlers:
- url: /.*
  script: auto
  secure: always
  redirect_http_response_code: 301
