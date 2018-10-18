from pathlib import Path

import zipfile

from sendmail import *


# From http://stackoverflow.com/questions/14568647/create-zip-in-python
def zip_files(data_path, zip_path, filepath_filter=lambda x: True):
    """ Create zip at zip_path from files with extension ext2zip located at
            data_path.
    """
    with zipfile.ZipFile("%s.zip" % (zip_path), "w") as zf:
        for filepath in data_path.glob('**/*'):
            if filepath.is_file():
                if filepath_filter(filepath):
                    zf.write(filepath, filepath.name)


def main():
    zip_path = Path("data")
    data_path = Path(
        "C:/Users/alistair/The Local Data Company/Footfall Phoenix - General/mmwave/prototype/capture_data/boardroom/raw/")
    zip_files(data_path, zip_path, )

    quit()
    Emailer("footfall-install-1@localdatacompany.com"
            ).send_mail_with_attachment("alistair@localdatacompany.com",
                                        "Data",
                                        "This is some data",
                                        str(zip_path) + ".zip",
                                        "data.zip")
    # send_email_with_payload()


if __name__ == "__main__":
    main()
