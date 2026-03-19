import requests

import json



# 1. Paste your exact Cloud Run URL

CLOUD_RUN_URL = "https://vanvikalp-engine-733206344564.us-central1.run.app/generate"



# 2. Paste the massive token you just copied from the terminal

TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImM0MWYxNDFhYTE5ZGYwYWM5N2RhYTU1ZTYwMDc2NmM0YzUzNjRjNDIiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiIzMjU1NTk0MDU1OS5hcHBzLmdvb2dsZXVzZXJjb250ZW50LmNvbSIsImF1ZCI6IjMyNTU1OTQwNTU5LmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwic3ViIjoiMTEzMTM4ODg3NTAzODEzNjcwOTQ0IiwiZW1haWwiOiJhaWRldmVsb3BtZW50YW5raXRAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImF0X2hhc2giOiJQZllTaWxjV2JPWnZFSmYzeTh4UU1nIiwiaWF0IjoxNzczOTQyMDM2LCJleHAiOjE3NzM5NDU2MzZ9.dfgMhOUD1IA_qfDqoywjTU-7WueM6b2-6e3y5VRY40YzQXv6zVUgiIHaMEL0y83r74PZ4ayWrNOpT6rj1LiW1-DrNHjQvjamrP9xh3dWvxHPrWmOIJy7KKVjZpPabPJ6skv_dZJVN5UFPZuTwVI2drWQK8AqgS6xAcz5PnrszNOJhUg7c_cPbOFYiwHgKgnls2HwPIuQiCQteof_jvcVeZOd3J9W3TpyeU72q69q74m0js0pUSvGaxHLVtBdTErWPoPs4_dfmUKVbRF_ozU-9i87Xn-NgPE_A7QaEKCAR7s8pR7TtOaZ-pWlH0CSVTsz9mIS6SjTLN4XIQVTre_qKA"



# 3. We add the token to the headers to prove to Google Cloud who we are

headers = {

    "Authorization": f"Bearer {TOKEN}",

    "Content-Type": "application/json"

}



payload = {

    "prompt": "We are modernizing the Calcutta University heritage campus. The courtyard floods, the grid is overloaded, and we need to cool the old buildings without adding solar panels. Provide an ESG strategy."

}



print(f"Sending Authenticated POST request to: {CLOUD_RUN_URL}")

print("Waking up the Engine... (this may take a few seconds)")



try:

    response = requests.post(CLOUD_RUN_URL, json=payload, headers=headers, timeout=300)

    

    if response.status_code == 200:

        print("\n=== SUCCESS: VALID JSON RECEIVED FROM CLOUD ===")

        print(json.dumps(response.json(), indent=4))

    else:

        print(f"\n=== API REJECTED REQUEST ===")

        print(f"Status Code: {response.status_code}")

        print(f"Error Message: {response.text}")



except requests.exceptions.RequestException as e:

    print(f"\nConnection Error: {e}")