import requests

def main():
    print("➭ I Am An KHAN SIR Extractor Script.")
    print("➭ To Use Me, Enter Your AUTH CODE Below:")
    
    token = input("Enter AUTH CODE: ")
    
    headers = {
        "Host": "admin2.khanglobalstudies.com",
        "authorization": f"Bearer {token}",
        "client-id": "5f439b64d553cc02d283e1b4",
        "client-version": "21.0",
        "user-agent": "Android",
        "randomid": "385bc0ce778e8d0b",
        "client-type": "MOBILE",
        "device-meta": "{APP_VERSION:19.0,DEVICE_MAKE:Asus,DEVICE_MODEL:ASUS_X00TD,OS_VERSION:6,PACKAGE_NAME:xyz.penpencil.khansirofficial}",
        "content-type": "application/json; charset=UTF-8",
    }
    
    params = {
        "mode": "2",
        "filter": "false",
        "exam": "",
        "amount": "",
        "organisationId": "5f439b64d553cc02d283e1b4",
        "classes": "",
        "limit": "20",
        "page": "1",
        "programId": "5f476e70a64b4a00ddd81379",
        "ut": "1652675230446",
    }
    
    response = requests.get(
        "https://admin2.khanglobalstudies.com/api/user/v2/courses?medium=0",
        params=params,
        headers=headers,
    ).json()
    
    print("\nAvailable Batches:")
    batch_list = {}
    for data in response:
        batch_name = data["title"]
        batch_id = data["id"]
        batch_list[batch_id] = batch_name
        print(f"{batch_name} : {batch_id}")
    
    print("\nNow enter the Batch ID to download:")
    batch_id = input("Enter Batch ID: ")
    
    if batch_id not in batch_list:
        print("Invalid Batch ID! Exiting...")
        return
    
    response2 = requests.get(
        f"https://admin2.khanglobalstudies.com/api/user/courses/{batch_id}/lessons?medium=0",
        headers=headers,
    ).json()["lessons"]
    
    to_write = ""
    for data in response2:
        batch_names = data["videos"]
        for vish in batch_names:
            vids = vish["video_url"]
            name = vish["name"]
            to_write += f"{name}: {vids}\n"
    
    file_name = f"{batch_id}.txt"
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(to_write)
    
    print(f"\nBatch details saved in '{file_name}'.")

if __name__ == "__main__":
    main()
