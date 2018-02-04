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

# Fonction qui va regarder si le master préfère le nouvel etudiant (res = tuple(master, student))
# Par rapport a ses preferences (master_pref)
# Et modifira par la meme occasion le tuple prefEtu (array pref, booleen si il a un master) 
def prefer(result, res, master_pref, prefEtu):
	couple_master=[]; #tableau de tuple de tous les couples d'un meme master
	i=0; # iteration dans la tableau result
	while i < (len(result)): # Tant que i n'atteint pas la fin du tableau
		# print(result[i], (res[0]))
		if int(result[i][0])==int(res[0]): # Si le couple inclu la master en question
			couple_master.append(result.pop(i)); # On ajoute ce couple dans la tableau des couples du meme master
			# On le retire par la même occasion du tableau result
			i=i-1; #On decremente i car on vient d'enlever un element du tableau
		i=i+1;
	# print(len(couple_master));
	for i in range(len(couple_master)): # Pour tous les couples avec le meme master
		# Si l'index du nouveau couple a inserer est plus petit (donc le master prefere le nouveau)
		if master_pref[0].index(str(couple_master[i][1]))>master_pref[0].index(str(res[1])):
			sub=couple_master[i]; # Permet de sauvegarder le couple avant de l'ecraser
			couple_master[i]=res; # Remplace le couple moins interressant par le nouveau
			res=sub; # Le couple moins interressant devra être interroger à nouveau si il reste de la place dans le master
	prefEtu[res[1]]=(prefEtu[res[1]][0], False); # Le couple le moins interressant sera remi à False (car il est plus assigné avec un master)
	for i in range(len(couple_master)): # On va remettre tous les couples les plus interressant dans result
		prefEtu[int(couple_master[i][1])]=(prefEtu[int(couple_master[i][1])][0], True); # On met a True tous les etudiants figurant dans couple_master
		result.append(couple_master[i]);
	# print(result, res);
	return result, prefEtu; # On retourne le tableau result et les preferences des etudiants qui ont etaient modifie

# Fonction qui va regarder si il y a au moins un master qui à de la place
def masters_contains_false(preference_masters):
	# On boucle sur tous les masters
	for i in range(len(preference_masters)) :
		# Si il y en a un de False avec on return true
		if preference_masters[i][1]==False : 
			return True;
	return False; # Sinon on retourne false
	
# Fonction qui va appliquer l'algorithme de gale shapley
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
			res = (int(student_wish), i); # On forme un tuple (id Master, id Etudiant)
			# print(res);
			if prefSpe[int(student_wish)][1]==False: # Si il reste de la place dans le master
				result.append(res); # On ajoute le tuple dans le tableau de resultat
				# On ajoute un etudiant au nb d'etudiant du master
				addStudent=(prefSpe[int(student_wish)][0], prefSpe[int(student_wish)][1] ,prefSpe[int(student_wish)][2]+1);
				prefSpe[int(student_wish)]=addStudent;
				# Si le master à atteint la capacite max
				if prefSpe[int(student_wish)][2]==int(cap[int(student_wish)]):
					# Alors on met a True le master pour signifier que c'est complet
					prefSpe[int(student_wish)]=(prefSpe[int(student_wish)][0],True);
				# On met aussi l'etudiant à True pour signifier qu'il a un master
				prefEtu[i]=(prefEtu[i][0], True); 
				# print(prefSpe[int(student_wish)][1]);
			else : # Sinon sa veut dire que le master est complet
				# On va donc appeler la fonction result afin de voir si le master prefere le nouvel etudiant
				result, prefEtu = prefer(result, res, prefSpe[int(student_wish[0])], prefEtu);
		i=i+1;
	# print(result);
	return result;

if __name__ == '__main__':
	prefSpe = openPref("TestPrefSpe.txt", 2);
	# print(prefSpe);
	prefEtu = openPref("TestPrefEtu.txt", 1)[0];
	# print(prefEtu);
	resultat=gale_shapley_impl(prefSpe, prefEtu);
	print(resultat);


