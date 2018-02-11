#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from operator import itemgetter

def lectureFichier(s): # Definition d'une fonction, avec un parametre (s). Ne pas oublier les ":"
	monFichier = open(s, "r"); # Ouverture en lecture. Indentation par rapport a la ligne d'avant (<-> bloc).
	contenu = monFichier.readlines(); # Contenu contient une liste de chainces de caracteres, chaque chaine correspond a une ligne       
	monFichier.close(); #Fermeture du fichier
	leng = len(contenu);
	for i in range(leng):
		contenu[i]=contenu[i].split();
	return contenu;

def openPref(my_file, nb_ligne_a_suppr):
	contenu=lectureFichier(my_file);
	capacity = None;
	if my_file == sys.argv[2]:
		capacity = contenu[1][1:];
		capacity = list(map(int, capacity))
	contenu = contenu[nb_ligne_a_suppr:]; #Supprimer les premières ligne des fichier (NbEtu 11)
	leng = len(contenu);
	for i in range(leng):
		prefs = list(map(int, contenu[i][2:]))
		contenu[i] = [prefs, False, 0];
	# print(contenu); 
	return contenu,capacity;

def contains(pref):
	for i in range(len(pref)):
		if pref[i][1] == False:
			return pref[i];
	return None

# Fonction qui va regarder si le master préfère le nouvel etudiant (res = tuple(master, student))
# Par rapport a ses preferences (master_pref)
# Et modifira par la meme occasion le tuple prefEtu (array pref, booleen si il a un master) 
def prefer(result, res, master_pref, prefEtu):
	couple_master=[]; #tableau de tuple de tous les couples d'un meme master
	i=0; # iteration dans la tableau result
	for i in range (len(result)) :
		if result[i][0] == res[0]: #Si on trouve un couple de meme master dans le tableau resultat
			if master_pref[0].index(result[i][1])>master_pref[0].index(res[1]): #Si l'index de celui-ci est inferieur
				prefEtu[res[1]]=(prefEtu[res[1]][0], True); #Le nouvel etudiant sera assigne à un master
				sub=result[i]; #Subtitue
				result[i]=res; #Insertion du nouveau couple
				res=sub; #Et le couple sortant sera de nouveau controle
	prefEtu[res[1]]=(prefEtu[res[1]][0], False); # L'etudiant le moins interressant sera remi à False (car il est plus assigné avec un master)
	return result, prefEtu; # On retourne le tableau result et les preferences des etudiants qui ont etaient modifie
	
# Fonction qui va regarder si le master préfère le nouvel etudiant (res = tuple(master, student))
# Par rapport a ses preferences (master_pref)
# Et modifira par la meme occasion le tuple prefEtu (array pref, booleen si il a un master) 
def prefer_cote_parcours(result, res, student_pref, prefSpe, capacity):
	couple_master=[]; #tableau de tuple de tous les couples d'un meme master
	i=0; # iteration dans la tableau result
	copy_res=res;
	for i in range (len(result)):
		if result[i][0]==res[0]:
			if student_pref[0].index(result[i][1])>student_pref[0].index(res[1]):
				prefSpe[res[1]]=(prefSpe[res[1]][0], prefSpe[res[1]][1], prefSpe[res[1]][2]+1);
				if prefSpe[res[1]][2]==capacity[res[1]]:
					prefSpe[res[1]]=(prefSpe[res[1]][0], True, prefSpe[res[1]][2]);
				sub = result[i];
				result[i]=res;
				res=sub;
	if(copy_res!=res):
		prefSpe[res[1]]=(prefSpe[res[1]][0], False, prefSpe[res[1]][2]-1);
	return result, prefSpe; # On retourne le tableau result et les preferences des etudiants qui ont etaient modifie

# Fonction qui va regarder si il y a au moins un master qui à de la place
def masters_contains_false(preference_masters):
	# On boucle sur tous les masters
	# print(preference_masters);
	for i in range(len(preference_masters)) :
		# Si il y en a un de False avec on return true
		if preference_masters[i][1]==False : 
			return True;
	return False; # Sinon on retourne false

def etu_contains_false(pref_etu):
	print(prefEtu);
	for i in range(len(pref_etu)):
		if pref_etu[i][1]==False:
			return True;
	return False;
	
# Fonction qui va appliquer l'algorithme de gale shapley cote etudiant
def gale_shapley_impl(prefSpe,prefEtu):
	i=0; 
	result = []; # this will hold tuple of our result (Student,Master)
	lenEtu = len(prefEtu);
	cap = prefSpe[1]; # get the capacity of each branch in a list 1D
	prefSpe = prefSpe[0]; # get the branches matrix 2D 
	while masters_contains_false(prefSpe): # Tant qu'il y a un master qui aura de la place
		if(i>=len(prefEtu)): # Si la valeur i dépasse l'indice max du tableau des etudiants
			i=0; # on reini i
		while(prefEtu[i][1]==True): # On va passer les Etudiants qui auront deja un master
			i=i+1; # On incrément i pour passer à l'tudiant suivant
			if(i>=len(prefEtu)): # On controle si on ne depasse pas 
				i=0;
		courantEtu = prefEtu[i]; # On va prendre les preference de l'etudiant qui n'as pas encore de master
		while prefEtu[i][1]==False: # Tant qu'on lui a pas assigner un master
			# On enleve le master que prefere l'etudiant afin de verifier les dispo
			student_wish = courantEtu[0].pop(0); # On recupere le master qu'il prefere
			res = (student_wish, i); # On forme un tuple (id Master, id Etudiant)
			# print(res);
			if prefSpe[student_wish][1]==False: # Si il reste de la place dans le master
				result.append(res); # On ajoute le tuple dans le tableau de resultat
				# On ajoute un etudiant au nb d'etudiant du master
				addStudent=(prefSpe[student_wish][0], prefSpe[student_wish][1] ,prefSpe[student_wish][2]+1);
				prefSpe[student_wish]=addStudent;
				# Si le master à atteint la capacite max
				if prefSpe[student_wish][2]==cap[student_wish]:
					# Alors on met a True le master pour signifier que c'est complet
					prefSpe[student_wish]=(prefSpe[student_wish][0],True);
				# On met aussi l'etudiant à True pour signifier qu'il a un master
				prefEtu[i]=(prefEtu[i][0], True); 
				# print(prefSpe[int(student_wish)][1]);
			else : # Sinon sa veut dire que le master est complet
				# On va donc appeler la fonction result afin de voir si le master prefere le nouvel etudiant
				result, prefEtu = prefer(result, res, prefSpe[student_wish], prefEtu);
		i=i+1;
	# print(result);
	return result;

# Fonction qui va appliquer l'algorithme de gale shapley cote parcours
def gale_shapley_parcours(prefSpe,prefEtu):
	i=0; 
	result = []; # this will hold tuple of our result (Student,Master)
	lenEtu = len(prefEtu);
	cap = prefSpe[1]; # get the capacity of each branch in a list 1D
	prefSpe = prefSpe[0]; # get the branches matrix 2D 
	while masters_contains_false(prefSpe): # Tant qu'il y a un master qui aura de la place
		if(i>=len(prefSpe)): # Si la valeur i dépasse l'indice max du tableau des parcours
			i=0; # on reini i
		while(prefSpe[i][1]==True): # On va passer les parcours qui sont plein
			i=i+1; # On incrément i pour passer à l'etudiant suivant
			if(i>=len(prefSpe)): # On controle si on ne depasse pas 
				i=0;
		courantSpe = prefSpe[i]; # On va prendre les preference du parcours qui n'est pas plein
		while prefSpe[i][1]==False: # Tant qu'on lui a pas assigner un etudiant
			# On enleve l'etudiant prefere du master
			etu_wish = courantSpe[0].pop(0); # On recupere l'etudiant prefere
			# print(etu_wish, len(prefEtu));
			res = (etu_wish, i); # On forme un tuple (id Etudiant, id Master)
			# print(res);
			if prefEtu[etu_wish][1]==False: # Si il reste de la place dans le master
				result.append(res); # On ajoute le tuple dans le tableau de resultat
				# On ajoute un etudiant au nb d'etudiant du master
				addStudent=(prefSpe[i][0], prefSpe[i][1] ,prefSpe[i][2]+1);
				prefSpe[i]=addStudent;
				# Si le master à atteint la capacite max
				if prefSpe[i][2]==cap[i]:
					# Alors on met a True le master pour signifier que c'est complet
					prefSpe[i]=(prefSpe[i][0],True, prefSpe[i][2]);
				# On met aussi l'etudiant à True pour signifier qu'il a un master
				prefEtu[etu_wish]=(prefEtu[etu_wish][0], True); 
				# print(prefSpe[int(master_wish)][1]);			
			else : # Sinon sa veut dire que l'étudiant à déjà un master
				# On va donc appeler la fonction result afin de voir si l'étudiant préfère le nouveau master
				result, prefSpe = prefer_cote_parcours(result, res, prefEtu[etu_wish], prefSpe, cap);
		i=i+1;
	# print(result);
	return result;

def reverse(result):
	for i in range (len(result)):
		result[i]=(result[i][1], result[i][0]);
	return result;

if __name__ == '__main__':
	prefSpe = openPref(sys.argv[2], 2);
	prefEtu = openPref(sys.argv[1], 1)[0];
	cote_parcours_prefSpe = openPref(sys.argv[2], 2);
	cote_parcours_prefEtu = openPref(sys.argv[1], 1)[0];
	print(cote_parcours_prefEtu);
	# print(prefEtu);
	print("Côté étudiant : ");
	resultat=gale_shapley_impl(prefSpe, prefEtu);
	resultat=reverse(resultat);
	print(sorted(resultat, key=itemgetter(0)));
	resultat_cote_parcours=gale_shapley_parcours(cote_parcours_prefSpe,cote_parcours_prefEtu);
	# resultat_cote_parcours=reverse()
	print(sorted(resultat_cote_parcours, key=itemgetter(0)));


