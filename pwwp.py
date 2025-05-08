import requests
import asyncio
import aiohttp
import json
import os
import logging
from typing import Dict, Any, List  # Import Dict, Any, and List from typing module

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def fetch_pwwp_data(session: aiohttp.ClientSession, url: str, headers: Dict = None, params: Dict = None, data: Dict = None, method: str = 'GET') -> Any:
    max_retries = 3
    for attempt in range(max_retries):
        try:
            async with session.request(method, url, headers=headers, params=params, json=data) as response:
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientError as e:
            logging.error(f"Attempt {attempt + 1} failed: aiohttp error fetching {url}: {e}")
        except Exception as e:
            logging.exception(f"Attempt {attempt + 1} failed: Unexpected error fetching {url}: {e}")

        if attempt < max_retries - 1:
            await asyncio.sleep(90 ** attempt)
        else:
            logging.error(f"Failed to fetch {url} after {max_retries} attempts.")
            return None

async def process_pwwp_chapter_content(session: aiohttp.ClientSession, chapter_id, selected_batch_id, subject_id, schedule_id, content_type, headers: Dict):
    url = f"https://api.penpencil.co/v1/batches/{selected_batch_id}/subject/{subject_id}/schedule/{schedule_id}/schedule-details"
    data = await fetch_pwwp_data(session, url, headers=headers)
    content = []

    if data and data.get("success") and data.get("data"):
        data_item = data["data"]

        if content_type in ("videos", "DppVideos"):
            video_details = data_item.get('videoDetails', {})
            if video_details:
                name = data_item.get('topic', '')
                videoUrl = video_details.get('videoUrl') or video_details.get('embedCode') or ""
                if videoUrl:
                    line = f"{name}:{videoUrl}"
                    content.append(line)

        elif content_type in ("notes", "DppNotes"):
            homework_ids = data_item.get('homeworkIds', [])
            for homework in homework_ids:
                attachment_ids = homework.get('attachmentIds', [])
                name = homework.get('topic', '')
                for attachment in attachment_ids:
                    url = attachment.get('baseUrl', '') + attachment.get('key', '')
                    if url:
                        line = f"{name}:{url}"
                        content.append(line)

        return {content_type: content} if content else {}
    else:
        logging.warning(f"No Data Found For Id - {schedule_id}")
        return {}

async def fetch_pwwp_all_schedule(session: aiohttp.ClientSession, chapter_id, selected_batch_id, subject_id, content_type, headers: Dict) -> List[Dict]:
    all_schedule = []
    page = 1
    while True:
        params = {
            'tag': chapter_id,
            'contentType': content_type,
            'page': page
        }
        url = f"https://api.penpencil.co/v2/batches/{selected_batch_id}/subject/{subject_id}/contents"
        data = await fetch_pwwp_data(session, url, headers=headers, params=params)

        if data and data.get("success") and data.get("data"):
            for item in data["data"]:
                item['content_type'] = content_type
                all_schedule.append(item)
            page += 1
        else:
            break
    return all_schedule

async def process_pwwp_chapters(session: aiohttp.ClientSession, chapter_id, selected_batch_id, subject_id, headers: Dict):
    content_types = ['videos', 'notes', 'DppNotes', 'DppVideos']
    
    all_schedule_tasks = [fetch_pwwp_all_schedule(session, chapter_id, selected_batch_id, subject_id, content_type, headers) for content_type in content_types]
    all_schedules = await asyncio.gather(*all_schedule_tasks)
    
    all_schedule = []
    for schedule in all_schedules:
        all_schedule.extend(schedule)
        
    content_tasks = [
        process_pwwp_chapter_content(session, chapter_id, selected_batch_id, subject_id, item["_id"], item['content_type'], headers)
        for item in all_schedule
    ]
    content_results = await asyncio.gather(*content_tasks)

    combined_content = {}
    for result in content_results:
        if result:
            for content_type, content_list in result.items():
                if content_type not in combined_content:
                    combined_content[content_type] = []
                combined_content[content_type].extend(content_list)

    return combined_content

async def get_pwwp_all_chapters(session: aiohttp.ClientSession, selected_batch_id, subject_id, headers: Dict):
    all_chapters = []
    page = 1
    while True:
        url = f"https://api.penpencil.co/v2/batches/{selected_batch_id}/subject/{subject_id}/topics?page={page}"
        data = await fetch_pwwp_data(session, url, headers=headers)

        if data and data.get("data"):
            chapters = data["data"]
            all_chapters.extend(chapters)
            page += 1
        else:
            break

    return all_chapters

async def process_pwwp_subject(session: aiohttp.ClientSession, subject: Dict, selected_batch_id: str, selected_batch_name: str, all_subject_urls: Dict[str, List[str]], headers: Dict):
    subject_name = subject.get("subject", "Unknown Subject").replace("/", "-")
    subject_id = subject.get("_id")
    all_subject_urls[subject_name] = []

    chapters = await get_pwwp_all_chapters(session, selected_batch_id, subject_id, headers)
    
    chapter_tasks = []
    for chapter in chapters:
        chapter_name = chapter.get("name", "Unknown Chapter").replace("/", "-")
        chapter_tasks.append(process_pwwp_chapters(session, chapter["_id"], selected_batch_id, subject_id, headers))

    chapter_results = await asyncio.gather(*chapter_tasks)

    for chapter, chapter_content in zip(chapters, chapter_results):
        chapter_name = chapter.get("name", "Unknown Chapter").replace("/", "-")

        for content_type in ['videos', 'notes', 'DppNotes', 'DppVideos']:
            if chapter_content.get(content_type):
                content = chapter_content[content_type]
                content.reverse()
                all_subject_urls[subject_name].extend(content)

async def main():
    print("➭ Physics Wallah TXT Extractor Script.")
    print("➭ Please Enter Your Authentication Token or Phone Number Below.\n")
    
    # Get token or phone number from the user
    token_or_phone = input("Enter Your Token or Phone Number: ").strip()

    if not token_or_phone:
        print("Error: Token or Phone Number cannot be empty.")
        return

    headers = {
        'Host': 'api.penpencil.co',
        'client-id': '5eb393ee95fab7468a79d189',
        'client-version': '1910',
        'user-agent': 'Mozilla/5.0 (Linux; Android 12; M2101K6P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36',
        'randomid': '72012511-256c-4e1c-b4c7-29d67136af37',
        'client-type': 'WEB',
        'content-type': 'application/json; charset=utf-8',
    }

    async with aiohttp.ClientSession() as session:
        try:
            if token_or_phone.isdigit() and len(token_or_phone) == 10:
                phone = token_or_phone
                data = {
                    "username": phone,
                    "countryCode": "+91",
                    "organizationId": "5eb393ee95fab7468a79d189"
                }
                try:
                    async with session.post(f"https://api.penpencil.co/v1/users/get-otp?smsType=0", json=data, headers=headers) as response:
                        await response.read()
                    
                except Exception as e:
                    print(f"Error : {e}")
                    return

                print("ENTER OTP YOU RECEIVED")
                otp = input("Enter OTP: ").strip()

                payload = {
                    "username": phone,
                    "otp": otp,
                    "client_id": "system-admin",
                    "client_secret": "KjPXuAVfC5xbmgreETNMaL7z",
                    "grant_type": "password",
                    "organizationId": "5eb393ee95fab7468a79d189",
                    "latitude": 0,
                    "longitude": 0
                }

                try:
                    async with session.post(f"https://api.penpencil.co/v3/oauth/token", json=payload, headers=headers) as response:
                        access_token = (await response.json())["data"]["access_token"]
                        print(f"Physics Wallah Login Successful ✅\n\nSave this Login Token for future usage: {access_token}")
                    
                except Exception as e:
                    print(f"Error : {e}")
                    return

            else:
                access_token = token_or_phone
            
            headers['authorization'] = f"Bearer {access_token}"
        
            print("Enter Your Batch ID:")
            batch_id = input("Batch ID: ").strip()

            url = f"https://api.penpencil.co/v3/batches/{batch_id}/details"
            batch_details = await fetch_pwwp_data(session, url, headers=headers)

            if batch_details and batch_details.get("success"):
                subjects = batch_details.get("data", {}).get("subjects", [])
                all_subject_urls = {}

                subject_tasks = [process_pwwp_subject(session, subject, batch_id, batch_id, all_subject_urls, headers) for subject in subjects]
                await asyncio.gather(*subject_tasks)
                
                with open(f"{batch_id}.txt", 'w', encoding='utf-8') as f:
                    for subject in subjects:
                        subject_name = subject.get("subject", "Unknown Subject").replace("/", "-")
                        if subject_name in all_subject_urls:
                            f.write('\n'.join(all_subject_urls[subject_name]) + '\n')
                                
                print(f"Data successfully saved to {batch_id}.txt")
            else:
                print(f"Error fetching batch details: {batch_details.get('message')}")
        except Exception as e:
            logging.exception(f"An unexpected error occurred: {e}")
        finally:
            await session.close()

if __name__ == "__main__":
    asyncio.run(main())