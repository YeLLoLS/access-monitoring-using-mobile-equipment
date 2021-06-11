import requests

query = """mutation {
  createPost(numeUser:"%s", cheie:"deschide usa"){
    post{
      numeUser
      cheie
      timpArg
      dataArg
      }
    }
  }
"""

url = 'https://192.168.0.153/graphql'


def req(numeUser):
    query2 = query % (str(numeUser))
    requests.post(url, json={'query': query2})
