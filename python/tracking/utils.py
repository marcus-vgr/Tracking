import pickle

def open_pickle(ifile: str):
    if not ifile.endswith(".pickle"):
        ifile += ".pickle"
    with open(ifile, "rb") as f:
        return pickle.load(f)

def save_pickle(ofile: str, data):
    if not ofile.endswith(".pickle"):
        ofile += ".pickle"
    with open(ofile, "wb") as f:
        pickle.dump(data, f)