             _       _            
            (_)     | |           
  _ __  _ __ _ _ __ | |_ ___ _ __ 
 | '_ \| '__| | '_ \| __/ _ \ '__|
 | |_) | |  | | | | | ||  __/ |   
 | .__/|_|  |_|_| |_|\__\___|_|   
 | |                              
 |_|                              


############## images ##############
Sur windows, au lieu de renseigner manuellement le chemin de l'image à modifier,
il est possible de cliquer glisser une image directement sur l'icone de l'exécutable.


################ DPI ###############
Le script est calibré pour une densité de points par pouces (DPI) de 203.
Pour changer ce paramètre, changer la valeur PRINTER_DPI dans main.py.


############ config.cfg ############
Pour ne pas avoir a renseigner la largeur du papier à chaque boucle,
un fichier nommé config.cfg doit exister dans le même dossier que le script / exécutable.
Le format du congig doit être:

[Settings]
PAPER_WIDTH = largeur_du_papier

La largeur du papier doit être exprimée en pouces.
Pour convertir une valeur mesurée en centimètres en pouces,
utiliser le script cm_inch_converter.py.


########### troubleshoot ###########
Pour recréer un .exe ou faire fonctionner le script suivre le protocole suivant:

1/ Ouvrir le terminal dans le dossier du script
2/ py -m venv .venv
3/ .venv/Scripts/activate
3/ pip install -r requirements.txt
4/ pyinstaller --onefile --icon=icons/printer.ico --name "printer" main.py                    
5/ pyinstaller --onefile cm_inch_convert.py
6/ Récupérer les exécutables dans le dossier dist
