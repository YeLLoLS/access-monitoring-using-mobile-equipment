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

url = 'http://192.168.0.153:5000/graphql'


def req(numeUser):
    query2 = query % (str(numeUser))
    print(query2)
    requests.post(url, json={'query': query2})
