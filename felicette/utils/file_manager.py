import tempfile
import os

workdir = os.path.join(os.path.expanduser("~"), "felicette-data")
data_path = os.path.join(workdir, "LC81390462020136")

if not os.path.exists(data_path):
	os.mkdir(data_path)

def save_to_file(content, filename):
	file_path = os.path.join(data_path, filename)
	with open(file_path, 'w') as f:
		data = 'some data to be written to the file'
		f.write(data)
	f.close()

def data_file_exists(filename):
	file_path = os.path.join(data_path, filename)
	return os.path.exists(file_path)