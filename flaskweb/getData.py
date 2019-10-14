from flaskweb import db

def getServices(name):
    cursor = db.Services.find({'Type': name})
    services = []
    for i in cursor:
        # Use the services that contain description and coordinate
        if i['Type'] != 'hotlines':
            if i['What'] != 'Unknown' and i['Latitude'] != 'Unknown' and i['Longitude'] != 'Unknown':
                services.append(i)
        else:
            if i['What'] != 'Unknown':
                services.append(i)
    return services

def getInfo(service_name, id_):
    data = getServices(service_name)
    for document in data:
        if str(document.get('_id')) == id_:
            return document