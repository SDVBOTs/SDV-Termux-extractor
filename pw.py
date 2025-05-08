import requests

def get_batches(auth_code):
    headers = {
        'Host': 'api.penpencil.xyz',
        'authorization': f"Bearer {auth_code}",
        'client-id': '5eb393ee95fab7468a79d189',
        'client-version': '12.84',
        'user-agent': 'Android',
        'randomid': 'e4307177362e86f1',
        'client-type': 'MOBILE',
        'device-meta': '{APP_VERSION:12.84,DEVICE_MAKE:Asus,DEVICE_MODEL:ASUS_X00TD,OS_VERSION:6,PACKAGE_NAME:xyz.penpencil.physicswalb}',
        'content-type': 'application/json; charset=UTF-8',
    }

    params = {
        'mode': '1',
        'filter': 'false',
        'exam': '',
        'amount': '',
        'organisationId': '5eb393ee95fab7468a79d189',
        'classes': '',
        'limit': '20',
        'page': '1',
        'programId': '',
        'ut': '1652675230446',
    }

    response = requests.get('https://api.penpencil.xyz/v3/batches/my-batches', params=params, headers=headers).json().get("data", [])
    return response

def get_subjects(batch_id, auth_code):
    headers = {
        'Host': 'api.penpencil.xyz',
        'authorization': f"Bearer {auth_code}",
        'client-id': '5eb393ee95fab7468a79d189',
        'client-version': '12.84',
        'user-agent': 'Android',
        'randomid': 'e4307177362e86f1',
        'client-type': 'MOBILE',
        'device-meta': '{APP_VERSION:12.84,DEVICE_MAKE:Asus,DEVICE_MODEL:ASUS_X00TD,OS_VERSION:6,PACKAGE_NAME:xyz.penpencil.physicswalb}',
        'content-type': 'application/json; charset=UTF-8',
    }

    response = requests.get(f'https://api.penpencil.xyz/v3/batches/{batch_id}/details', headers=headers).json().get("data", {}).get("subjects", [])
    return response

def get_batch_contents(batch_id, subject_id, page, auth_code):
    headers = {
        'Host': 'api.penpencil.xyz',
        'authorization': f"Bearer {auth_code}",
        'client-id': '5eb393ee95fab7468a79d189',
        'client-version': '12.84',
        'user-agent': 'Android',
        'randomid': 'e4307177362e86f1',
        'client-type': 'MOBILE',
        'device-meta': '{APP_VERSION:12.84,DEVICE_MAKE:Asus,DEVICE_MODEL:ASUS_X00TD,OS_VERSION:6,PACKAGE_NAME:xyz.penpencil.physicswalb}',
        'content-type': 'application/json; charset=UTF-8',
    }

    params = {'page': page, 'tag': '', 'contentType': 'exercises-notes-videos', 'ut': ''}
    response = requests.get(f'https://api.penpencil.xyz/v2/batches/{batch_id}/subject/{subject_id}/contents', params=params, headers=headers).json().get("data", [])
    return response

def save_batch_contents(batch_name, subject_data):
    with open(f"{batch_name}.txt", 'a') as file:
        for data in subject_data:
            class_title = data["topic"]
            class_url = data["url"].replace("d1d34p8vz63oiq", "d3nzo6itypaz07").replace("mpd", "m3u8").strip()
            file.write(f"{class_title}: {class_url}\n")

def main():
    auth_code = input("Enter your Auth Code: ")
    
    # Step 1: Fetch Batches
    batches = get_batches(auth_code)
    if not batches:
        print("No batches found.")
        return

    print("Your Batches:")
    for batch in batches:
        print(f"{batch['name']} : {batch['_id']}")

    batch_id = input("Enter the Batch ID to download: ")

    # Step 2: Fetch Subjects
    subjects = get_subjects(batch_id, auth_code)
    if not subjects:
        print("No subjects found for this batch.")
        return

    print("Subjects:")
    for subject in subjects:
        print(f"{subject['subject']} : {subject['_id']}")

    subject_id = input("Enter the Subject ID to fetch contents: ")

    # Step 3: Fetch Contents and Save to File
    page = 1
    all_subject_data = []
    while True:
        subject_data = get_batch_contents(batch_id, subject_id, page, auth_code)
        if not subject_data:
            break
        all_subject_data.extend(subject_data)
        page += 1

    if all_subject_data:
        batch_name = next((batch['name'] for batch in batches if batch['_id'] == batch_id), 'Unknown_Batch')
        save_batch_contents(batch_name, all_subject_data)
        print(f"Contents saved to {batch_name}.txt")
    else:
        print("No content found for this subject.")

if __name__ == "__main__":
    main()
