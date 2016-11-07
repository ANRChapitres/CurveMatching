# CurveMatching


Chers utilisateurs,

Voici les prémices du code qui vous permet d'établir des profils de courbes en fonction des chapitres d'un groupe de textes. Nous avons testé ces outils sur les œuvres de Zola. Pour les utiliser (c'est encore une version bêta), voilà comment faire :

Avant tout :

    avoir Java 7 minimum installé,
    avoir python 3 installé, avec notamment la librairie matplotlib

Première étape : génération des données avec vos textes :

Pour comparer vos données, l'ordinateur va avoir besoin de les rendre interprétables : il va tokéniser les textes, évaluer la taille des chapitres et la masse de mots dans chacun des chapitres, et rendre l'ensemble des données comparables entre elles en transformant le nombre de mots relatif des chapitres pour chaque roman en pourcentages. Par exemple, pour comparer un roman R1 de quatre chapitres et un autre R2 de vingt-cinq chapitres, et voir comment évolue la masse des mots pour chaque roman (savoir si les chapitres du début sont plus courts dans l'un, etc.), R1 qui aura 10 mots sur 100 totaux au chapitre 1 comprendra comme donnée 10% de mots à 25% du roman, et R2 qui aura 100 mots sur 1000 au chapitre 20 aura 10% à 80% du roman.

Ce calcul se fait en Java, et le code temporaire que nous avons n'appelle pas encore le script Python suivant (mais ça ne saurait tarder). Vous pouvez télécharger le paquet ici. Vous devez placer vos textes en .txt dans le dossier "Fichiers". Ensuite, si vous n'avez pas d'IDE comme Eclipse ou NetBeans préinstallés, vous devez aller dans votre terminal et entrer les commandes suivantes :
