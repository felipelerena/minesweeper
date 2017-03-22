from requests import put, get

if __name__ == '__main__':
    print("creating new game")
    res = put("http://localhost:5000/games/1",
              data={"rows": 10, "cols": 10, "mines": 5})
    print(res.json())

    print("getting game 1")
    res = get("http://localhost:5000/games/1")
    print(res.json())
