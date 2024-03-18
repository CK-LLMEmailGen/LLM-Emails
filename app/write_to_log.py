import pytz

data_upload_log = "logs/data_upload.log"
file_read_log = "logs/file_read.log"
gcp_log = "logs/gcp.log"
gemini_log = "logs/gemini.log"
generated_mails_log = "logs/generated_mails.log"
error_log = "logs/log_error.log"

def get_time() -> str:
    try:
        timezone = pytz.timezone('Asia/Kolkata')
        current_time = datetime.now(timezone)
        return current_time.strftime("%Y-%m-%d_%H:%M:%S")
    except Exception as e:
        with open(error_log, "a") as log_file:
            log_file.write(f"\n\n\nDatetime exception:\n{e}\n\n\n")

def write_to_file(filepath : str = "" , text : str = ""):
    try:
        with open(filepath, "a") as file:
            file.write(f"\n\n\n{get_time()}:\n{text}\n\n\n")
    except Exception as e:
        with open(error_log, "a") as log_file:
            log_file.write(f"\n\n\nLogs exception occured at {get_time()}:\n{e}\n\n\n")