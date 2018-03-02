# Webhook
## Normalize name estados, municipios
## And get lat and lon base on corner

The webhook expose three directions:
* *_edo_*: Return correct state name. Parameters:
  * _nombre_ : State name
  > /edo/?nombre=@flow.response1
* *_mun_*: Search municipio base on state. Parameters:
  * _estado_: Number of state, returned it in edo query
  * _nombre_ : Municipio name
  > /mun/?estado=@contact.rp_state_number&nombre=@flow.response2

* *_corner_*:Return lat and long base on two streets and municipio. Parameters:
  * _street_a_: First street
  * _street_b_: Second street
  * _municipio_: Municipio name
  > /corner/?street_a=@flow.response3&street_b=@flow.response4&municipio=@contact.rp_municipio

* *_country_*: Return correct country name. Parameters:
  * _nombre_ : Country name
  * _lng_ : One of [spa","eng","hol","por"]
  > /country/?nombre=@flow.response1&lng=spa
