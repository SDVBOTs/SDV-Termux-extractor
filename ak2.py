import requests

def apni_kaksha_extractor():
    print("➭ I Am An Apni Kaksha TXT Extractor Script.")
    print("➭ Please Enter Your Authentication Token Below.\n")
    
    # Get token from the user
    token = input("Enter Your Token: ").strip()

    if not token:
        print("Error: Token cannot be empty.")
        return

    # Set headers
    headers1 = {
        "Host": "spec.apnikaksha.net",
        "token": token,
        "origintype": "web",
        "user-agent": "Android",
        "usertype": "2",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
    }

    try:
        # Fetch batch data
        response1 = requests.get(
            "https://spec.apnikaksha.net/api/v2/my-batch", headers=headers1
        ).json()

        if 'data' not in response1:
            raise ValueError("Invalid response: 'data' not found in batch API response")

        response1 = response1["data"]["batchData"]

        print("\nBatch Name : Batch ID")
        for data in response1:
            print(f"`{data['batchName']}` : `{data['id']}`")

        # Get batch ID
        batch_idid = input("\nEnter Batch ID: ").strip()

        # Fetch subject data
        response2 = requests.get(
            f"https://spec.apnikaksha.net/api/v2/batch-subject/{batch_idid}",
            headers=headers1,
        ).json()

        if 'data' not in response2:
            raise ValueError("Invalid response: 'data' not found in subject API response")

        response2 = response2["data"]["batch_subject"]

        print("\nSubject Name : Subject ID")
        for data in response2:
            print(f"{data['subjectName']} : `{data['id']}`")

        # Get subject ID
        lesson_idid = input("\nEnter Subject ID: ").strip()

        # Ask for class or notes
        check_is = input("\nWhat do you want (class for Videos, notes for Notes): ").strip()

        # Fetch topic data
        response3 = requests.get(
            f"https://spec.apnikaksha.net/api/v2/batch-topic/{lesson_idid}?type={check_is}",
            headers=headers1,
        ).json()

        if 'data' not in response3:
            raise ValueError("Invalid response: 'data' not found in topic API response")

        response3 = response3["data"]["batch_topic"]

        to_write = ""
        for data in response3:
            topic_id = data["id"]
            if check_is == "class":
                response4 = requests.get(
                    f"https://spec.apnikaksha.net/api/v2/batch-detail/{batch_idid}?subjectId={lesson_idid}&topicId={topic_id}",
                    headers=headers1,
                ).json()

                if 'data' not in response4 or 'class_list' not in response4['data']:
                    raise ValueError("Invalid response: 'class_list' not found in batch-detail API response")

                response4 = response4["data"]["class_list"]["classes"]
                for element in response4:
                    lesson_url = element["lessonUrl"]
                    lesson_name = element["lessonName"].replace(":", " ")

                    # Fetch video token using lesson_id
                    video_token_response = requests.get(
                        f"https://spec.apnikaksha.net/api/v2/livestreamToken?base=web&module=batch&type=brightcove&vid={element['id']}",
                        headers=headers1,
                    ).json()

                    # Handle token response
                    video_token = video_token_response.get("data", {}).get("token", None)
                    if not video_token:
                        print(f"Skipping video: Token not found for {lesson_name}")
                        continue

                    # Generate video URL using lesson_url and token
                    video_url = f"https://edge.api.brightcove.com/playback/v1/accounts/6415636611001/videos/{lesson_url}/master.m3u8?bcov_auth={video_token}"
                    to_write += f"{lesson_name}: {video_url}\n"

            elif check_is == "notes":
                response4 = requests.get(
                    f"https://spec.apnikaksha.net/api/v2/batch-notes/{batch_idid}?subjectId={lesson_idid}&topicId={topic_id}",
                    headers=headers1,
                ).json()

                if 'data' not in response4 or 'notesDetails' not in response4['data']:
                    raise ValueError("Invalid response: 'notesDetails' not found in batch-notes API response")

                response4 = response4["data"]["notesDetails"]
                for element in response4:
                    doc_url = element["docUrl"]
                    doc_title = element["docTitle"].replace(":", " ")
                    to_write += f"{doc_title}: {doc_url}\n"

        # Save to TXT file
        filename = f"{lesson_idid}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(to_write)

        print(f"\nData successfully saved to {filename}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Run the extractor
if __name__ == "__main__":
    apni_kaksha_extractor()