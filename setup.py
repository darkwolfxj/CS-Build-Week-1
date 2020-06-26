import cx_Freeze

executables = [cx_Freeze.Executable("pygol.py")]

cx_Freeze.setup(
    name="A bit Racey",
    options={"build_exe": {"packages":["pygame", "sys", "time", "random", "math"],
                           "include_files":[]}},
    executables = executables

    )