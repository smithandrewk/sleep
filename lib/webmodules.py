import subprocess
import os
from subprocess import CalledProcessError
from lib.webconfig import *
import json

def score_wrapper(scoring_function, step, total_steps, msg, *args):
    """ Used by generator in 'main_score' to wrap pipeline functions in order to
        generate progress steps

    Args:
        scoring_function (function): pipeline function to call
        step (int): step number of this function
        total_steps (int): total number of steps in current pipeline
        msg (str): Message to display when function completes (display msg for next step)
        model (str, optional): If scoring with a model, provide which model to use. Defaults to None.

    Returns:
        str: text event stream string providing the progress of the pipeline
    """
    try:
        scoring_function(*args)
    #TODO raise exceptions in functions and use message
    except Exception as exc:
        print(f'ERROR step {step}')
        # return error message
        return f"data:0\tStep {step} In Function: {scoring_function.__name__} - {exc}\n\n"
        
    # return progress and the message for next step
    return f'data:{int(step/total_steps*100)}\tStep {step+1} - {msg}\n\n'

# functions for before and after pipeline
def unzip_upload(filename, iszip):
    # remove old files if they exist
    subprocess.run(['mkdir', '-p', f'data/{RAW_DIR}'])
    if iszip:
        args = ['cp', os.path.join(UPLOAD_FOLDER, filename), 'data/Unscored.zip']
        subprocess.run(args, check=True)
        args = ['unzip', '-j', 'data/Unscored.zip', '-d', f'./data/{RAW_DIR}']
        subprocess.run(args, check=True)        
    else: 
        args = ['cp', os.path.join(UPLOAD_FOLDER, filename), f'data/{RAW_DIR}/']
        subprocess.run(args, check=True)
def move_to_download_folder(new_filename):
    args = ['sh', '-c', 
            f"cd data/ && zip -r ../{DOWNLOAD_FOLDER}/{new_filename} {FINAL_SCORED_DIR}"]
    subprocess.run(args, check=True)
    
def archive_files(date):
    args = ['sh', '-c', 
            f"cd data/ && zip -r ../{ARCHIVE_FOLDER}/{date}.zip {FINAL_SCORED_DIR} {RAW_DIR}"]
    subprocess.run(args, check=True)

def clean_workspace(filename):
    args = ['rm', '-rf', 'data', f'from-client/{filename}']
    subprocess.run(args, check=True)

def email_results(email):
    import smtplib

    SENDER = 'AuroraProjectEmail@gmail.com'
    PASSWORD = 'kxfiusttkwlwneii'
    RECIEVER = email

    with smtplib.SMTP('smtp.gmail.com', 587) as s:
        s.ehlo()
        s.starttls()
        s.ehlo()

        s.login(SENDER, PASSWORD)  # app password
        subject = 'Data Scoring Complete'
        body = 'Your data has been successfully scored'
        msg = f'Subject: {subject}\n\n{body}'

        s.sendmail(SENDER, RECIEVER, msg)
        
def valid_extension(filename, iszip):
    if iszip:
        return filename.endswith(ALLOWED_EXTENSIONS['ZIP'])
    else:
        return (filename.endswith(ALLOWED_EXTENSIONS['XLS']) 
                or filename.endswith(ALLOWED_EXTENSIONS['XLSX']))
def init_dir(db):
    db.create_all()
    try:
        subprocess.run(['mkdir', '-p', UPLOAD_FOLDER])
        subprocess.run(['mkdir', '-p', DOWNLOAD_FOLDER])
        subprocess.run(['mkdir', '-p', ARCHIVE_FOLDER])

    except CalledProcessError as exc:
        print(f'Error initializing directory: {exc}')
        exit(1)
def unzip_zdb_upload(filename, iszip):
    subprocess.run(['mkdir', '-p', f'data/{RAW_ZDB_DIR}'])
    if iszip:
        args = ['cp', os.path.join(UPLOAD_FOLDER, filename), 'data/UnscoredZDB.zip']
        subprocess.run(args, check=True)
        args = ['unzip', '-j', 'data/Unscored.zip', '-d', f'./data/{RAW_ZDB_DIR}']
        subprocess.run(args, check=True)        
    else: 
        args = ['cp', os.path.join(UPLOAD_FOLDER, filename), f'data/{RAW_ZDB_DIR}']
        subprocess.run(args, check=True)
def valid_zdb_extension(filename, iszip):
    if iszip:
        return filename.endswith(ALLOWED_EXTENSIONS['ZIP'])
    else:
        return filename.endswith(ALLOWED_EXTENSIONS['ZDB'])  