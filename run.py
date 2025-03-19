
import sys
import requests

from wengyl_mcga import check_news  # 匯入函式


def notify_discord_greenshoots_webhook(msg):
    url = 'https://discord.com/api/webhooks/1345960695493034004/eKY2pE-0YYcYGn3n1_SSEfdJ9IvLm_RjbIhOSWEPld6C2H_hrhypIUsJYBU0yBbRzlK_'
    headers = {"Content-Type": "application/json"}
    data = {"content": msg, "username": "Greenshoots News"}
    res = requests.post(url, headers = headers, json = data) 
    if res.status_code in (200, 204):
            print(f"Request fulfilled with response: {res.text}")
    else:
            print(f"Request failed with response: {res.status_code}-{res.text}")

def generate_msg():
    new_announcements = check_news()  # 呼叫函式取得新公告
    if new_announcements:
        msg = '\n\n'.join(
            f"{announcement['title']} {announcement['source']} \n{announcement['link']}"
            for announcement in new_announcements
        )
        return msg
    return None

def job():
    
    msg = generate_msg()
    if msg is None:
        print("No new news")
        return
    if len(msg) > 2000:
        msg_list = [msg[i:i+2000] for i in range(0, len(msg), 2000)]
        for msg in msg_list:
            notify_discord_greenshoots_webhook(msg)
        return
    else:
        notify_discord_greenshoots_webhook(msg)
        return


def signal_handler(sig, frame):
    global running
    print('Stopping the scheduler...')
    running = False
    sys.exit(0)

if __name__ == "__main__":

    job()
