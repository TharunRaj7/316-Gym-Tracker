import pandas as pd

def insertRes(db):
    df = pd.read_csv('data/Resources_data.csv')
    
    for i in range(len(df)):
        des = str(df['Description'][i])
        loc = str(df['Gym'][i])
        type = str(df['Type'][i])

        query = "insert into Resources (ResourceName, ResourceType, Location) values ('%s', '%s', '%s')" % (des, type, loc)
        db.engine.execute(query)


#insertRes()