// Renvoie vrai si 'c' est un entier >= 0
function isIntegerPlus(c) {
    var is_ok = true;
    var i = 0;

    if (c.length == 0) {
        return false;
    }

    while (is_ok && (i < c.length)) {
        is_ok = ((c[i] >= '0') && (c[i] <= '9'));
        i++;
    }
    return is_ok;
}

// Vérifie que tous les types sont définis
function areDefined(type, debut, taille, pas) {
    var retour = [];

    if (type == undefined) {
        retour.push(false);
        retour.push("Erreur : type n'est pas défini");
    }
    if (debut == undefined) {
        if (retour.length == 0) {
            retour.push(false);
        }
        retour.push("Erreur : debut n'est pas défini");
    }
    if (taille == undefined) {
        if (retour.length == 0) {
            retour.push(false);
        }
        retour.push("Erreur : pas n'est pas défini");
    }
    if (pas == undefined) {
        if (retour.length == 0) {
            retour.push(false);
        }
        retour.push("Erreur : pas n'est pas défini");
    }
    return retour;
}

// Vérifie que les types sont valides
function areValid(retour, type, debut, taille, pas) {
    if ((type != 'ta_as') && (type != 'ta_af') && (type != 'ta_ar')) {
        if (retour.length == 0) {
            retour.push(false);
        }
        retour.push("Erreur : type ne peut être que 'ta_as', 'ta_af ou 'ta_ar'");
    }
    if (!isIntegerPlus(debut)) {
        if (retour.length == 0) {
            retour.push(false);
        }
        retour.push("Erreur : debut doit être un entier supérieur ou égal à 0");
    }

    if (!isIntegerPlus(taille)) {
        if (retour.length == 0) {
            retour.push(false);
        }
        retour.push("Erreur : taille doit être un entier supérieur ou égal à 800");
    }
    else if (taille < 800) {
        if (retour.length == 0) {
            retour.push(false);
        }
        retour.push("Erreur : taille doit être un entier supérieur ou égal à 800");
    }

    if (!isIntegerPlus(pas)) {
        if (retour.length == 0) {
            retour.push(false);
        }
        retour.push("Erreur : pas doit être un entier supérieur ou égal à 0");
    }

    return retour;
}

// Vérifie les options
// Renvoie True si tout est Ok
// Renvoie False et le message d'ereur correspondant
function options(infos) {
    var type = infos['type'];
    var debut = infos['debut'];
    var taille = infos['taille'];
    var pas = infos['pas'];

    var retour = [];


    retour = retour.concat(areDefined(type, debut, taille, pas));

    if (retour.length == 0) {
        retour = areValid(retour, type, debut, taille, pas);
    }

    if (retour.length == 0) {
        retour.push(true)
    }


    return retour;
}

// Renvoie l'extension du fichier
function getExtension(fichier) {
    var extArray = [];
    var is_ok = true;
    var is_point = false;
    var i = fichier.length - 1;
    var nom = fichier;
    var ext = "";

    while (is_ok && !is_point && i > 0) {
        is_ok = ((nom[i] != '/') && (i > 0));
        is_point = nom[i] == "."
        extArray.unshift(nom[i]);
        i--;
    }

    for (var j = 0; j < extArray.length; j++) {
        ext = ext + extArray[j];
    }

    return ext;
}

exports.options = options;
exports.getExtension = getExtension;
