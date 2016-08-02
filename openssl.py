from subprocess import call
from cipher import all_ciphers
import os


def crypto(files, password, cipher, decrypt=False, delete=False):
  """Main input function for openssl core commands.

  Args:
      files (list): List of files to perform encryption/decryption.
      password (str): Pass key to encrypt/decrypt files.
      cipher (str): Algorithm to be used for encryption/decryption.
      decrypt (bool): Value set to True for decryption else False.
      delete (bool): Boolean value when set true deletes source files after
          successful operation.

  Returns:
      status (list): List of bools each corresponding to the status of each
          file operation.
  """

  if decrypt:
    status = dec(files, password, cipher, delete)
  else:
    status = enc(files, password, cipher, delete)

  return status


def enc(files, password, cipher, delete=False):
  """Implemetation of encryption.

  Args:
      files (list): List of files to perform encryption.
      password (str): Pass key to encrypt files.
      cipher (str): Algorithm to be used for encryption.
      delete (bool): Boolean value when set true deletes source files after
          successful operation.

  Returns:
      out_status (list): List of bools each corresponding to the status of each
          file operation.
  """

  out_status = []
  for file_ in files:
    command = ["openssl", cipher, "-in", file_, "-out",
               "{}{}".format(file_, ".enc"), "-k", str(password)]
    if check_commnad(files, password, cipher):
      command_out = call(command)
      if delete:
        delete_file(file_)
      out_status.append(True)
    else:
      out_status.append(False)

  return out_status


def dec(files, password, cipher, delete=False):
  """Implemetation of encryption.

  Args:
      files (list): List of files to perform decryption.
      password (str): Pass key to decrypt files.
      cipher (str): Algorithm to be used for decryption.
      delete (bool): Boolean value when set true deletes source files after
          successful operation.

  Returns:
      out_status (list): List of bools each corresponding to the status of each
          file operation.
  """

  out_status = []
  for file_ in files:
    temp_file = "{}{}".format(file_, "XXXtemp6969")
    command = ["openssl", cipher, "-d", "-in", file_, "-out",
               temp_file, "-k", str(password)]
    if check_commnad(files, password, cipher):
      command_out = call(command)
      if command_out == 0:
        move_file(temp_file, file_.strip(".enc"))
      else:
        delete_file(temp_file)
    else:
      out_status.append(False)

  return out_status


def compress_crypt(directory, password, cipher, delete=False):
  """Compresses a given directory contents to tar.gz and then encrypts the
  tar file.

  If inputs are correct, it will write an encrypted tar file of the dir
  provided.

  Args:
      directory (str): Directory to perform encryption.
      password (str): Pass key to encrypt directory.
      cipher (str): Algorithm to be used for encryption.
      delete (bool): Boolean value when set true deletes source directory after
          successful operation.

  Returns:
      bool: True if successful else False.
  """

  outfile = "{}{}".format(directory, ".tar.gz")
  command = ["tar", "-czf", outfile, directory]
  if check_commnad(directory, password, cipher):
    call(command)
    crypto([outfile], password, cipher)
    return True
  else:
    return False


def check_commnad(files, password, cipher):
  """Checks whether the files, password, and cipher method are correct.
  Checks whether files/dir exists.
  Checks whether password is not empty.
  Checks whether ciper is present in valid link or not.

  Args:
      files (list/str): List of files or directory to validate .
      password (str): Pass key to validate.
      cipher (str): Algorithm to be used for encryption.

  Returns:
      bool : True if all args are correct else False.
  """

  if password is None or password == "":
    return False

  if cipher not in all_ciphers:
    return False

  if type(files) == list:
    if files:
      for file_ in files:
        if not os.path.isfile(file_):
          return False
    else:
      return False
  else:
    if not os.path.exists(files):
      return False
  return True


def delete_file(file_):
  """Deletes a SINGLE FILE from the disk which is provided in Args.
  DOES NOT deletes directories.
  """
  status = call(["rm", file_])


def move_file(source, destination):
  """Moves a FILE from `source` to `destination`.
  Currently used to rename a file(temp file created during decryption)
  """
  status = call(['mv', source, destination])
