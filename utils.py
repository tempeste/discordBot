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
    command = "/home/pwserver/pwserver details"
    result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
    status_output = result.stdout

    # Remove ANSI escape codes for more reliable regex matching
    ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
    cleaned_output = ansi_escape.sub('', status_output)

    # Extracting the 'Internet IP', 'CPU Used' and 'Mem Used' sections
    internet_ip = re.search(r"Internet IP:\s*(.+)", cleaned_output)
    cpu_usage = re.search(r"CPU Used:\s*(.+?)%", cleaned_output)
    mem_usage = re.search(r"Mem Used:\s*(.+)%", cleaned_output)
    server_status_search = re.search(r"Status:\s*(\w+)", cleaned_output)

    internet_ip = internet_ip.group(1) if internet_ip else "Not Found"
    cpu_usage = f"CPU Used: {cpu_usage.group(1)}%" if cpu_usage else "Not Found"
    mem_usage = f"Mem Used: {mem_usage.group(1)}%" if mem_usage else "Not Found"
    server_status = server_status_search.group(1) if server_status_search else "Not Found"

    return internet_ip, cpu_usage, mem_usage, server_status

async def restart_palworld_server():
    command = "/home/pwserver/pwserver restart"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    try:
        stdout, stderr = await asyncio.wait_for(asyncio.to_thread(process.communicate), timeout=120)  # Timeout in seconds
        return process.returncode, stdout, stderr
    except asyncio.TimeoutError:
        return None, None, "Timeout"