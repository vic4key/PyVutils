import PyVutils as vu

def fn(file_path, file_directory, file_name):
    print("`%s` - `%s` - `%s`" % (file_path, file_directory, file_name))
    return

vu.recursive_directory(".", fn)
