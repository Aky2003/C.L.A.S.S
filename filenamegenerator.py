def filena(latitude, longitude):
    import gridtogeo
    address = gridtogeo.addressleav(latitude, longitude)

    if address is None:
        return "UnknownLocation"

    filename = ""
  
    if "," in address:
        for char in address:
            if char == ",":
                break
            filename += char
    else:
        filename = address 

    return filename

