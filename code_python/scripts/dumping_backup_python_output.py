from datetime import datetime # Timestamp output
import os
from code_python.scripts.config.folder_paths import FOLDER_PATH

# Prepare for dumping files
CODE_FILES_PATH  = f'{FOLDER_PATH}/scripts'

CALCULATION_PATH   = [
    f"{CODE_FILES_PATH}/config/parameters.py",
    f"{CODE_FILES_PATH}/setup/timestep_setup.py",
    f"{CODE_FILES_PATH}/setup/calculation_setup.py",
    f"{CODE_FILES_PATH}/preprocessing/get_hdf5_data.py",
    f"{CODE_FILES_PATH}/preprocessing/custom_advanced_functions.py",
    f"{CODE_FILES_PATH}/mainloop/run_calculation.py",
]

OUTPUT_FILE_PATH = f'{FOLDER_PATH}/records'

process_txt: str = ""

def dump_process(txt: str):
    global process_txt
    process_txt += "\n" + txt
    print(txt)


def save(time_start: datetime, output_path):
    now_local = datetime.now().astimezone()
    offset = now_local.strftime("%z")[:3]

    time_start_str = time_start.strftime("%H:%M:%S")
    time_end_str = now_local.strftime("%H:%M:%S")
    date_str = now_local.strftime("%Y/%m/%d")

    time_output = now_local.strftime("%Y%m%d_%H%M%S")
    output_file = f"{OUTPUT_FILE_PATH}/run_{time_output}_UTC{offset}.txt"

    with open(output_file, "w", encoding="utf-8") as outfile:
        FILES_TO_PRINT = []
        if output_path == "calculation_path":
            FILES_TO_PRINT = CALCULATION_PATH
        else:
            raise ValueError("output_path enables 'calculation_path', 'plotting_path' and 'all_path'.")

        outfile.write(f"Code dump created on {time_start_str} - {time_end_str} {date_str} (UTC{offset})\n")
        outfile.write("────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────\n")

        for filename in FILES_TO_PRINT:
            filepath = os.path.join(CODE_FILES_PATH, filename)
            if os.path.exists(filepath):
                outfile.write(f"\n═══════ {filename} ═══════\n\n")
                with open(filepath, "r", encoding="utf-8") as infile:
                    outfile.write(infile.read())
                    outfile.write("\n"
                                  "\n────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────\n"
                                  "\n"
                                  "\n"
                                  "\n"
                                  "\n"
                                  "\n────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────\n")

            else:
                outfile.write(f"\n═══════ {filename} (NOT FOUND) ═══════\n\n")
        # Separator
        outfile.write("Process Log:\n")

        # Process log
        outfile.write(process_txt)

        print(f"Save record to {output_file}")