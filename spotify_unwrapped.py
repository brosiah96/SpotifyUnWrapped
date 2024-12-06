import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Replace these with your Spotify Developer credentials
CLIENT_ID = 'CLIENT_ID'
CLIENT_SECRET = 'CLIENT_SECRET'
REDIRECT_URI = 'http://localhost:8080/callback'  # Must match the URI in your Spotify app settings

# Scope to access top tracks and artists
SCOPE = 'user-top-read user-read-recently-played'

# Authenticate and initialize Spotify client
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope=SCOPE))


def get_top_artists_and_tracks():
    print("Fetching your top artists and tracks...")

    # Get top artists
    top_artists = sp.current_user_top_artists(limit=10, time_range='long_term')
    print("\nYour Top Artists:")
    for idx, artist in enumerate(top_artists['items']):
        print(f"{idx + 1}. {artist['name']}")

    # Get top tracks
    top_tracks = sp.current_user_top_tracks(limit=10, time_range='long_term')
    print("\nYour Top Tracks:")
    for idx, track in enumerate(top_tracks['items']):
        print(f"{idx + 1}. {track['name']} by {', '.join(artist['name'] for artist in track['artists'])}")

    return top_artists['items'], top_tracks['items']


def pretty_print_top_artists_and_tracks(top_artists, top_tracks):
    print("\n### Your Top Artists (Markdown Table):\n")
    print("| Rank | Artist Name        |")
    print("|------|--------------------|")
    for idx, artist in enumerate(top_artists):
        print(f"| {idx + 1:4} | {artist['name']:18} |")

    print("\n### Your Top Tracks (Markdown Table):\n")
    print("| Rank | Track Name         | Artist(s)             |")
    print("|------|--------------------|-----------------------|")
    for idx, track in enumerate(top_tracks):
        artist_names = ", ".join(artist['name'] for artist in track['artists'])
        print(f"| {idx + 1:4} | {track['name'][:18]:18} | {artist_names[:20]:20} |")


def generate_mermaid_diagram(top_artists, top_tracks):
    print("\n### Mermaid Representation\n")
    print("```mermaid")
    print("graph TD")
    print("    A[Top Artists and Tracks] --> B[Artists]")
    print("    A --> C[Tracks]")

    for idx, artist in enumerate(top_artists):
        print(f"    B --> B{idx}[{artist['name']}]")

    for idx, track in enumerate(top_tracks):
        track_name = track['name'].replace('"', '\\"')  # Escape quotes
        artist_names = ", ".join(artist['name'] for artist in track['artists'])
        print(f"    C --> C{idx}[\"{track_name} by {artist_names}\"]")
    print("```")


if __name__ == "__main__":
    # Get top artists and tracks
    top_artists, top_tracks = get_top_artists_and_tracks()

    # Pretty print the results
    pretty_print_top_artists_and_tracks(top_artists, top_tracks)

    # Generate Mermaid diagram
    generate_mermaid_diagram(top_artists, top_tracks)
