import requests

query = """mutation {
  createPost(numeUser:%s, cheie:"t7w!zC*F-JaNdRgUjXn2r5u8x/A?D(G+KbPeShVmYp3s6v9y$B&E)H@McQfTjWn"){
    post{
      numeUser
      cheie
      timpArg
      dataArg
      ipAdd
      }
    }
  }
"""

url = 'https://ip-to-rpi/'


def req(numeUser):
    query2 = query % (numeUser)
    requests.post(url, json={'query': query2})
