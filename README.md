# CurveMatching


Chers utilisateurs,

Voici les prémices du code qui vous permet d'établir des profils de courbes en fonction des chapitres d'un groupe de textes. Nous avons testé ces outils sur les œuvres de Zola. Pour les utiliser (c'est encore une version bêta), voilà comment faire :

Avant tout :

   -avoir Java 7 minimum installé,
   -avoir Python 3 installé, avec notamment la librairie matplotlib

1. Première étape : génération des données avec vos textes :

	Pour comparer vos données, l'ordinateur va avoir besoin de les rendre interprétables : il va tokéniser les textes, 	évaluer la taille des chapitres et la masse de mots dans chacun des chapitres, et rendre l'ensemble des données comparables entre elles en transformant le nombre de mots relatif des chapitres pour chaque roman en pourcentages. Par exemple, pour comparer un roman R1 de quatre chapitres et un autre R2 de vingt-cinq chapitres, et voir comment évolue la masse des mots pour chaque roman (savoir si les chapitres du début sont plus courts dans l'un, etc.), R1 qui aura 10 mots sur 100 totaux au chapitre 1 comprendra comme donnée 10% de mots à 25% du roman, et R2 qui aura 100 mots sur 1000 au chapitre 20 aura 10% à 80% du roman.

	Ce calcul se fait en Java, et le code temporaire que nous avons n'appelle pas encore le script Python suivant (mais ça ne saurait tarder). Vous pouvez télécharger le paquet ici. Vous devez placer vos textes en .txt dans le dossier "Fichiers"du dossier où a été compilé le .jar, c'est-à-dire le dossier "build". Ensuite, si vous n'avez pas d'IDE comme Eclipse ou NetBeans préinstallés, vous devez aller dans votre terminal et entrer les commandes suivantes  (je fais sous Linux, mais je mets les commandes théoriques, sans les avoir testées, de mac et windows, qui normalement sont les mêmes que celles de Linux ici) :

    cd /votreBrancheUtilisateur/votreNomUtilisateur/leFichierOuVousAvezTelechargelLeProjet/build/
    java -jar curveMatching.jar

	(En gros ici, dans la première commande vous dites à votre ordinateur d'aller prendre les données d'un dossier précis, puis vous lui demandez d'interpréter le fichier .jar avec un interpréteur Java)

	Vous vous retrouvez donc normalement avec un dossier de fichiers générés dans le dossier "build", intitulé "CSVOutput". Si vous souhaitez que j'ajoute une option pour que vous puissiez choisir votre chemin de sortie (l'endroit où vous allez recevoir les nouveaux fichiers générés), n'hésitez pas à me le dire.

2. Deuxième étape : Time Series Clustering (ou création de groupes de courbes)

	C'est là que Python est utile. Avec le programme en python suivant, qui sera bientôt intégré au java précédent (ce qui fera une étape en moins), vous allez créer des profils de courbes. Autrement dit, vous allez fournir des données individuelles obtenues avec les fichiers générés précédemment, et lui demander de trouver leurs points communs, et comment ses données peuvent être regroupées et comparées. Pour plus de détails sur le procédé, voir le billet ici.

	Tous les fichiers dont vous avez besoin sont déjà dans le dossier téléchargé depuis github. Il vous suffit cette fois de faire deux choses :

   -aller dans le dossier "Python" qui est dans le dossier du projet téléchargé, ouvrir le dossier "datasets" et remplacer le fichier déjà présent "output.csv" par celui que vous venez de générer lors de l'étape précédente. Même chose pour le fichier "names.txt".
    -exécuter les commandes suivantes :
        (si vous êtes toujours dans votre terminal et que vous n'avez pas changé de chemin de fichiers entre temps)
            
			cd Python
        OU si vous avez changé de chemin ou éteint votre terminal,
		
    		cd /votreBrancheUtilisateur/votreNomUtilisateur/leFichierOuVousAvezTelechargelLeProjet/build/
	
        une fois dans le dossier "Python", vous pouvez exécuter la commande suivante :
            
			python3 CurveMatching.py

	Vous vous retrouvez alors avec vos profils de courbes dynamiques (zoom possible, export en différents formats etc.).

3. Configuration du fichier .py :

	Par défaut, le fichier python CurveMatching.py est configuré pour une analyse lourde (très lourde) des données, que je vous déconseille d'exécuter si votre ordinateur est déjà naturellement lent. Par défaut, sur une grosse machine, tel que le fichier est configuré, l'analyse met presque quinze minutes.

	Si vous avez besoin de résultats rapides, voici ce que vous devez changer dans le fichier .py (c'est très simple). Ouvrez le fichier .py avec n'importe quel éditeur de texte (brut de préférence) en faisant un clic-droit dessus. Vous vous retrouvez avec le code principal sous les yeux. Recherchez la ligne suivante :

	"mapOfTimeSeries=k_means_clust(data, namesArray,10,200,100)".

	Dans cette ligne, vous demandez à votre ordinateur de s'entraîner sur les données que vous lui fournissez. Ne touchez pas aux variables "data" et "namesArray", mais vous pouvez toucher au reste : le premier des trois chiffres correspond au nombre de courbes que vous voulez produire (ici 10). Le deuxième chiffre est ce qui donne le plus de mal à votre ordinateur : c'est le nombre de tours qu'il doit faire pour s'entraîner : vous pouvez le descendre autant que vous voulez, tant que c'est supérieur à 0. Enfin votre ordinateur va pour chaque ligne de données générer aléatoirement une fenêtre dans laquelle il va piocher ses résultats : vous pouvez diminuer la fenêtre. Cependant je ne vous le conseille pas, parce que le gain de temps n'est pas suffisamment important pour risquer de perdre en précision.

	Voilà ! Je vous rappelle qu'il s'agit d'une version très basique encore, et qu'elle sera appelée à changer beaucoup dans les mois à venir. Si vous avez la moindre question, n'hésitez pas à la poser sur la boîte mail de l'ANR.
