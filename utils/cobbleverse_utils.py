import subprocess
import re
import asyncio


async def check_cobbleverse_server():
    try:
        command = "/home/tempeste/Drive2_symlink/cobbleverse/mcserver details"
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        status_output = stdout.decode('utf-8')
        stderr_output = stderr.decode('utf-8')

        # If the command failed but we got output in stderr
        if process.returncode != 0:
            return (
                "Error", 
                "N/A", 
                "N/A", 
                "STOPPED" if "not running" in stderr_output.lower() else "ERROR"
            )

        # Remove ANSI escape codes for more reliable regex matching
        ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
        cleaned_output = ansi_escape.sub('', status_output)

        # Extracting the sections
        internet_ip = re.search(r"Internet IP:\s*(.+?):\d+", cleaned_output)
        cpu_usage = re.search(r"CPU Used:\s*(.+?)%", cleaned_output)
        mem_usage = re.search(r"Mem Used:\s*(.+)%", cleaned_output)
        server_status_search = re.search(r"Status:\s*(\w+)", cleaned_output)

        internet_ip = internet_ip.group(1) if internet_ip else "Not Found"
        cpu_usage = f"CPU Used: {cpu_usage.group(1)}%" if cpu_usage else "Not Found"
        mem_usage = f"Mem Used: {mem_usage.group(1)}%" if mem_usage else "Not Found"
        server_status = server_status_search.group(1) if server_status_search else "Not Found"

        return internet_ip, cpu_usage, mem_usage, server_status

    except Exception as e:
        return f"Error: {str(e)}", "N/A", "N/A", "ERROR"

async def start_cobbleverse_server():
    command = "/home/tempeste/Drive2_symlink/cobbleverse/mcserver start"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    try:
        stdout, stderr = await asyncio.wait_for(asyncio.to_thread(process.communicate), timeout=120)  # Timeout in seconds
        return process.returncode, stdout, stderr
    except asyncio.TimeoutError:
        return None, None, "Timeout"
    
async def stop_cobbleverse_server():
    command = "/home/tempeste/Drive2_symlink/cobbleverse/mcserver stop"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    try:
        stdout, stderr = await asyncio.wait_for(asyncio.to_thread(process.communicate), timeout=120)  # Timeout in seconds
        return process.returncode, stdout, stderr
    except asyncio.TimeoutError:
        return None, None, "Timeout"

async def restart_cobbleverse_server():
    command = "/home/tempeste/Drive2_symlink/cobbleverse/mcserver restart"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    try:
        stdout, stderr = await asyncio.wait_for(asyncio.to_thread(process.communicate), timeout=120)  # Timeout in seconds
        return process.returncode, stdout, stderr
    except asyncio.TimeoutError:
        return None, None, "Timeout"