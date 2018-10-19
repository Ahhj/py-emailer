from pathlib import Path

import zipfile
import click

from sendmail import *


# From http://stackoverflow.com/questions/14568647/create-zip-in-python
def zip_files(data_path, zip_path, filepath_filter=lambda x: True):
    """ Create zip at zip_path from files with extension ext2zip located at
        data_path.
    """
    with zipfile.ZipFile(str(zip_path), "w") as zf:
        for filepath in data_path.glob('**/*'):
            if filepath.is_file():
                if filepath_filter(filepath):
                    zf.write(filepath, filepath.name)


def click_str_to_path(ctx, param, value):
    return Path(value)


@click.command()
@click.option("--sender", "-s", type=str, default="")
@click.option("--recipients", "-r", type=str, default="")
@click.option("--subject", "-j", type=str, default="")
@click.option("--message", "-m", type=str, default="")
@click.option("--data_path", "-d", type=str, default="", callback=click_str_to_path)
@click.option("--extension", "-x", type=str, default="")
@click.option("--output_path", "-o", type=str, default="", callback=click_str_to_path)
def main(sender, recipients, subject, message, data_path, output_path, extension):
    zip_files(data_path, output_path, lambda x: extension in x)

    mail_params = recipients, subject, message, str(output_path), output_path.name
    Emailer(sender).send_mail_with_attachment(*mail_params)


if __name__ == "__main__":
    main()
