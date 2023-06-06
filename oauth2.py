import webbrowser
import webserver as ws
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session

def get_oauth2_token(client_id, client_secret):
    # redirect_uri = 'https://www.youtube.com/watch?v=aHuZ99bcaCg&t=0'
    # redirect_uri = 'https://example.com'
    redirect_uri = 'https://localhost:6969'

    authorization_base_url = "https://accounts.spotify.com/authorize"
    token_url = "https://accounts.spotify.com/api/token"
    scope = [
        # "user-read-email",
        # "playlist-read-collaborative",
        "playlist-modify-private"
    ]

    spotify = OAuth2Session(client_id, scope=scope, redirect_uri=redirect_uri)

    webServer = ws.HTTPServer(("localhost", ws.SERVER_PORT), ws.MyServer)

    thread = ws.threading.Thread(target=ws.create_server, args=(webServer,))
    thread.start()

    authorization_url, state = spotify.authorization_url(authorization_base_url)
    webbrowser.open(authorization_url)

    while "code" not in ws.ARGS:
        pass
    code = ws.ARGS["code"]
    state = ws.ARGS["state"]
    redirect_response = f"https://localhost:6969/?code={code}&state={state}"

    webServer.server_close()
    thread.join()

    # redirect_response = input('\n\nPaste the full redirect URL here: ')
    
    auth = HTTPBasicAuth(client_id, client_secret)

    # Fetch the access token
    token = spotify.fetch_token(token_url,
                                auth=auth,
                                authorization_response=redirect_response,
                               )

    # print("\n")

    # Fetch a protected resource, i.e. user profile
    r = spotify.get('https://api.spotify.com/v1/me')
    # print(r.content)
    return token['access_token']