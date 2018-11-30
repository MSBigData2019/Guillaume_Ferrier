# coding: utf-8
  
import pandas as pd
import re

#Populations / dept
popbydep=pd.read_csv("population.csv",names=["dept","label","countpopstr"], header=None)
popbydep["countpopint"]=popbydep["countpopstr"].apply(lambda x:re.sub(r'(\d)\s+(\d)', r'\1\2', x)).astype(int)
# tbd drop useless
# popbydep = popbydep.drop(["countpopstr"], axis=1)


# Specialistes
specialistes = pd.read_excel("Honoraires_totaux_des_professionnels_de_sante_par_departement_en_2016.xls", sheet_name="Spécialistes",names=["specialite","deptstr","effectif","honor","depass","fraisdepl","total"] )
specialistes["dept"]=specialistes["deptstr"].apply(lambda x:x[0:2])
# tbd drop useless
# specialistes = specialistes.drop(["deptstr","fraisdepl"], axis=1)


# cleanung des lignes avec Total en specialite ou en cumul departement
specialistes = specialistes[~specialistes["deptstr"].str.contains("TOTAL")]
specialistes = specialistes[~specialistes["specialite"].str.contains("TOTAL")]

# merge specialistes / population
# Suppression des lignes avec Total dans le département
mergesp = pd.merge(specialistes, popbydep, how='inner', on="dept")

# calculs indices utiles 
# -1- nb medecin de la specialité consideree /100 hab
mergesp["densit"] = 100. * mergesp.effectif / mergesp.countpopint
# TBD autres stats ??

# stats generales cumulees ??
# stats france groupby  sur specialite 
#cumulfrance= mergesp.groupby(['specialite']).agg({"effectif": "sum","honor": "sum","depass":"sum","total":"sum"})
#cumulfrance["tauxdep"] = (100 * cumulfrance.depass / cumulfrance.honor).round(1)
# TBD tri ?
#cumulfrance=cumulfrance.sort_values("tauxdep", asc ending=False)
# TBD autres indices ??
