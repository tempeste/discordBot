import subprocess
import re
import asyncio

def search_youtube(youtube, search_query):
    request = youtube.search().list(
        part="snippet",
        q=search_query,
        maxResults=10,
        type="video"
    )
    return request.execute()

async def check_palworld_server():
    command = "/pwserver details"
    result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
    status_output = result.stdout

    # Extracting the 'Internet IP' and 'Palworld Resource Usage' sections
    internet_ip = re.search(r"Internet IP:\s*(.+)", status_output).group(1)
    resource_usage = re.search(r"Palworld Resource Usage.+?CPU Used:\s*(.+?)Mem Used:\s*(.+)", status_output, re.DOTALL).group(0)
    
    # Extracting the server status
    server_status = re.search(r"Status:\s*(\w+)", status_output).group(1)

    return internet_ip, resource_usage, server_status

async def restart_palworld_server():
    command = "/pwserver restart"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    try:
        stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=120)  # Timeout in seconds
        return process.returncode, stdout, stderr
    except asyncio.TimeoutError:
        return None, None, "Timeout"