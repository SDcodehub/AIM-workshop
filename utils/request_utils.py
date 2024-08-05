import requests
import base64
from typing import Dict, List


def post_api(url, data):
    """
    Send a POST request to the specified URL with the given data.

    :param url: The URL to which the request is sent.
    :param data: The data to be sent with the POST request.
    :return: The response from the server.
    """
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
        return response.json()  # Return the JSON response if successful
    except requests.exceptions.HTTPError as e:
        print(f"An error occurred: {e}")
        print(f"{response.text}")
        return None
    
def get_api(url):
    """
    Send a GET request to the specified URL with the given data.

    :param url: The URL to which the request is sent.
    :return: The response from the server.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
        return response.json()  # Return the JSON response if successful
    except requests.exceptions.HTTPError as e:
        print(f"An error occurred: {e}")
        print(f"{response.text}")
        return None
    
def delete_api(url):
    """
    Send a DELETE request to the specified URL with the given data.

    :param url: The URL to which the request is sent.
    :return: The response from the server.
    """
    try:
        response = requests.delete(url)
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
        return response.json()  # Return the JSON response if successful
    except requests.exceptions.HTTPError as e:
        print(f"An error occurred: {e}")
        print(f"{response.text}")
        return None

def encode_file_to_base64(filename: str) -> str:
    """Encode file content to base64."""
    with open(filename, "rb") as file:
        return base64.b64encode(file.read()).decode("utf-8")
    
def is_pdf(filename: str) -> bool:
    """Check if the file is a PDF based on its extension."""
    return filename.lower().endswith(".pdf")

def upload_doc(url, collection_id: str, metadata: List[str], filename: str):
    """Upload a document to the specified collection."""
    url = f"{url}/collections/{collection_id}/documents"

    metadata_dict: Dict[str, str] = {}

    # Convert the list of "key=value" strings to a dictionary
    if metadata and len(metadata) > 0:
        metadata_dict = dict(pair.split("=") for pair in metadata)

    # Check if the file is a PDF and encode it if it is
    if is_pdf(filename):
        encoded_content: str = encode_file_to_base64(filename)
        format_type: str = "pdf"
    else:
        with open(filename, "r") as file:
            encoded_content = file.read()
        format_type: str = "txt"

    # Prepare the payload
    payload = {
        "metadata": metadata_dict,
        "content": encoded_content,
        "format": format_type,
    }

    # Make the POST request
    try:
        response = requests.post(url, json=[payload])
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
        return response.json()  # Return the JSON response if successful
    except requests.exceptions.HTTPError as e:
        print(f"An error occurred: {e}")
        print(f"{response.text}")
        return None