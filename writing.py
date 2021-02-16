import pandas as pd

def write_excel(data, outfile):
    """
    A function that writes the fit information of an array of experiments to a
    specified outfile.

    Input:
      data: an array of Experiment objects that may or may not have been fited
      outfile: the name of the file to which the data will be written
    """
    acros = [data[exp].acrophase for exp in data if data[exp].fitted]
    mesors = [data[exp].mesor for exp in data if data[exp].fitted]
    amps = [data[exp].amplitude for exp in data if data[exp].fitted]
    rs = [data[exp].r2 for exp in data if data[exp].fitted]
    df = pd.DataFrame([acros, mesors, amps, rs],
                      index = ["Acrophase", "Mesor", "Amplitude", "R^2"],
                      columns = [data[exp].name for exp in data if data[exp].fitted]
                     )
    df.to_excel(outfile)
