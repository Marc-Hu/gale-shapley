#!/usr/bin/env python
# -*- coding: utf-8 -*-

def lectureFichier(s): # Definition d'une fonction, avec un parametre (s). Ne pas oublier les ":"
	monFichier = open(s, "r"); # Ouverture en lecture. Indentation par rapport a la ligne d'avant (<-> bloc).
	contenu = monFichier.readlines(); # Contenu contient une liste de chainces de caracteres, chaque chaine correspond a une ligne       
	monFichier.close(); #Fermeture du fichier
	leng = len(contenu);
	for i in range(leng):
		contenu[i]=contenu[i].split();
	return contenu;

def openPref(nomFichier,nb_ligne_a_suppr):
	contenu=lectureFichier(nomFichier);
	cap = None;
	if nomFichier == "TestPrefSpe.txt":
		cap = contenu[1][1:];
	contenu = contenu[nb_ligne_a_suppr:]; #Supprimer les premières ligne des fichier (NbEtu 11)
	leng = len(contenu);
	for i in range(leng):
		contenu[i]=(contenu[i][2:],False,0); 
	return contenu,cap;

def contains(pref):
	for i in range(len(pref)):
		if pref[i][1] == False:
			return pref[i];
	return None
def check_full(prefSpe,cap,master_idx):
	prefSpe[master_idx][2] = prefSpe[master_idx][2] + 1;
	if prefSpe[master_idx][2] == cap[master_idx];
		prefSpe[master_idx][1] = True;	

def prefer(prefMaster,master_idx,std_idx,result):
	old = []
	for r in result: 
		if r[1] == master_idx:
			old.append(r); 

	# in this step we have the old master choosen by the student
	# no we need to check if the master prefere the std_idex than the old mached student-master
	# in the old list
	# if so we need to return true:
	# else return false
	
def gale_shapley_impl(prefSpe,prefEtu):
	result = []; # this will hold tuple of our result (Student,Master)
	lenEtu = len(prefEtu);
	cap = prefSpe[1]; # get the capacity of each branch in a list 1D
	prefSpe = prefSpe[0]; # get the branches matrix 2D 
	courantEtu = prefEtu[0]; # assing the first student tuple(list,False,nb)
	while(courantEtu != None): # while there is a student
		nb = courantEtu[2]; # get the number of choosed branches;
		master = courantEtu[0][nb]; # get the first master choosed by the student !
		if prefSpe[master][1] == False: # si le master est Libre
			r = (prefEtu.index(courantEtu),master);
			result.append(r);
			check_full(prefSpe,cap,master);
		elif 
		courantEtu = contains(prefEtu);

if __name__ == '__main__':
	prefSpe = openPref("TestPrefSpe.txt", 2);
	print(prefSpe);
	prefEtu = openPref("TestPrefEtu.txt", 1)[0];
	print(prefEtu);


