from spotifyclient import SpotifyClient

from credenziali import data

import os
os.system("cls")

SW_PL    = "2qH6bxa2Qq6iR0Kj7FLfvQ"
QUEUE_PL = "5nQAHce0rJzkCH7GlX6uqR"
COM_PL   = "0UfIcZPirghMmr9AIaysiM"

if __name__ == "__main__":

    spotify = SpotifyClient(data.client_id(), data.client_secret(), data.user_id())

    print("Avvio svuotamento playlist...")
    spotify.empty_playlist(QUEUE_PL)
    print("\nAvvio riempimento playlist...")
    spotify.random_fill_playlist(QUEUE_PL, SW_PL, 5)
    print("\nOperazione completata!")