import pandas as pd

def pre_process(Genre,Balance,NbrDeProduit,MembreActif,Age):
    if 'Femme' in Genre:
        Genre = Genre.replace('Femme',"0")
    else: 
        Genre = Genre.replace('Homme','1')
    if  'Oui'in MembreActif:
        MembreActif = MembreActif.replace('Oui', "0")
    else: 
        MembreActif = MembreActif.replace('Non', "1")
    
    
    my_dict = {'Genre':Genre,'Balance':int(Balance),'NbrDeProduit':NbrDeProduit,'MembreActif':MembreActif,'Age':Age}
    
    df = pd.DataFrame([my_dict])
    
    df['Age_Cat'] = pd.cut(df['Age'], bins=[x for x in range(0,100, 10)], labels=[x for x in range(1,10, 1)],right=True)
    df[['Age_Cat','MembreActif','NbrDeProduit','Genre']] = df[['Age_Cat','MembreActif','NbrDeProduit','Genre']].astype('object')
    return df