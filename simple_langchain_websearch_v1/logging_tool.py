import os 
import datetime
from langchain_community.tools import Tool

log_file = os.path.join("data", "log.txt")
current_datetime = datetime.datetime.now()

def save_log(log, current_datetime=current_datetime):
    if not os.path.exists(log_file):
        open(log_file, "w")

    with open(log_file, "a") as f:
        f.writelines([str(current_datetime) + " || " + log + "\n"])

    return "log saved"

logging_tool = Tool(
    name="Logging_Tool",
    func=save_log,
    description="This tool saves agent logs in log.txt file. The log format is: Query: ... || Used tool: ... || Agent's response: ... . Always use this tool to save logs!"
)
