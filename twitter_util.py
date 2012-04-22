# need to install dependencies on server

import twitter
api = twitter.Api(consumer_key='nmnjwvk2sVD6xQBVaMKzg',
consumer_secret='mWIam6qsGVoiFfh9MGTUboA8G1EyRk8IFUvmzSWMunk', access_token_key='14103281-uirUc767UEjO6pSToRqbvi6byNJKGppVqaf3BJv0k', access_token_secret='WwtwNwDyjnDeGlaPnokWxChR4rIocA5RQI5xIlAOM')

tweets = api.GetSearch(term='apple')

