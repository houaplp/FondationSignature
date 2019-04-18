# fftToTriangle
version 1.2

## Interface
L'unité des paramètres début, taille et pas à été précisée : ms.

## Verification des paramètres
Le serveur node.js vérifie si le paramètre "taille" est bien supérieur ou égal à 800. La version d'avant vérifiait uniquement s'il était positif ou nul, le programme python se chargeait du reste. 

## Corrections de bugs
### Déconnexion des sockets
#### Description
Les socket se déconnectait après un moment d'inactivité. Le problème venait surtout du client qui pouvait être amené à ne rien faire pendant un moment.

#### Solution
Mettre en place un système dit, en anglais, de Heart beat (battement de coeur). Ce principe consiste à ce que le serveur envoie régulièrement un message au client (ping) qui lui répond à son tour. Ainsi, on impose une activité de la part du client au serveur (et du serveur au client) ce qui permet d'éviter les déconnexions non voulues. Cela ne dérange pas si le client ferme son navigateur : dans ce cas, la connexion est belle et bien fermée

### La compression de répertoire/fichier volumineux
#### Description
Après une analyse de fichier ou de répertoire, le répertoire contenant les résultats peut être volumineux. L'utilisation de `child_process.exec(...)` est limité par une taille de buffer maximale.

#### Solution
Utiliser la fonction suivante : `child_process.spawn(...)`. Cette fonction comporte une gestion de buffer différente qui nous permet d'éviter ce problème. Pour pouvoir utilisé les symboles && avec cette fonction :
```javascript
var cmd = child_process.spawn("commande bash", {
    shell: true
});
```
Cette méthode permet, en plus, d'écrire les commandes sous forme de chaîne de caractère, donc pas d'écriture de tableaux.
[Documentation de child_process](https://nodejs.org/api/child_process.html)
