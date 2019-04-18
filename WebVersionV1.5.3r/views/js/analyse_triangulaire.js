// Ouverture du socket
var socket = io.connect("http://localhost:8000");

// Envoie les données du formulaire au serveur
// Attention : les fichiers ne sont pas envoyés
function sendFormData() {
    // Récupération des information de formulaire
    var debut = document.getElementById("debut_analyse").value;
    var type = "";
    var taille = document.getElementById("taille_analyse").value;
    var pas = document.getElementById("pas_analyse").value;

    // Récupération de la valeur selectionné
    if (document.getElementById("ta_af").checked) {
        type = "ta_af";
    }
    else if (document.getElementById("ta_ar").checked) {
        type = "ta_ar";
    }
    else {
        // Au cas où un malin avait désactivé le javascript avant de valider
        type = "ta_as";
        document.getElementById("ta_as").checked = true;
    }

    document.getElementById("progression_info").style.display = "table";

    socket.emit('ant_param', {
        debut: debut,
        type: type,
        taille: taille,
        pas: pas
    });
}

// Affiche les erreurs
function afficheErreurParam(rep, fichier) {
    var message = "";

    if (rep[0]) {
        message = "Paramètres valides."
    }
    else {
        document.getElementById("preparation_fichier").style.display = "none";
        document.getElementById("upload_fichier_info").style.display = "none";
        message = "<ul>"
        for (var i = 1; i < rep.length; i++) {
            if ((rep[i] != true) && rep[i] != false) {
                message = message + "<li class='parametre_erreur'>" + rep[i] + "</li>"
            }
        }

        message = message + "</ul>"
    }
    document.getElementById("validate_data").innerHTML = message;
}


function main() {
    var fichier;
    var taille;
    var unMO = 1048576;
    var data = new ArrayBuffer(0);
    var avancement = 0;
    var increment_avancement;
    var tl_avancement = document.getElementById('tl_avancement');
    var tl_taille = document.getElementById('tl_taille');
    // Le bouton de validation
    var info_archive = document.getElementById("info_archive");
    var valider = document.getElementById("analyse_t_valide");
    var console_debug = document.getElementById("cons_debug_zone");
    var download_archive = document.getElementById("download_archive");
    var execution_prog_attente = document.getElementById("execution_prog_attente");
    var zip_chargement = document.getElementById("zip_chargement");
    // Valeur par défaut du bouton radio
    document.getElementById("ta_as").checked = true;

    valider.addEventListener("click", function () {
        sendFormData();
    });

    socket.on('ping_serv', function (data) {
        socket.emit('pong_client', { balle: 1 });
    });

    socket.on('erreur_recep_fichier', function () {
        document.getElementById('upload_fichier_info').innerHTML = "Problème rencortré lors du téléversement du fichier";
    });


    socket.on('televersement_fichier_serv', function (info) {
        if (info['is_ok']) {
            tl_avancement.innerHTML = (Math.round(avancement / 1024)).toString();
            if (increment_avancement > taille) {
                increment_avancement = taille;
            }
            avancement += increment_avancement;
            taille -= increment_avancement;
            socket.emit('televersement_fichier', { file: fichier.name, octet: data.slice(avancement - increment_avancement, avancement) });
        }
        else {
            document.getElementById('upload_fichier_info').innerHTML = "Erreur rencontré lors du téléversment";
            avancement = 0;
        }
    });

    socket.on("validate_data", function (rep) {
        afficheErreurParam(rep);
        download_archive.style.display = "none";
        download_archive.innerHTML = "";
        info_archive.innerHTML = "";
        console_debug.innerHTML = "";

        // Pour régler le problème des listeners sur les socket
        if (rep[0]) {
            var fichierInput = document.getElementById("fichier_analyse");
            document.getElementById("preparation_fichier").style.display = "block";
            fichier = fichierInput.files[0];

            if (fichier === undefined) {
                document.getElementById("preparation_fichier").innerHTML = "<span class='parametre_erreur'>Erreur : il faut préciser un fichier<span>";
                document.getElementById("upload_fichier_info").style.display = "none";
            }
            else {
                document.getElementById("upload_fichier_info").style.display = "block";
                document.getElementById('preparation_fichier').innerHTML = "Préparation du fichier : <span id='prep_progress'></span> %";

                var fr = new FileReader();
                

                // Chargement du fichier avant envoie
                fr.onprogress = function (e) {
                    var progression = (e.loaded / e.total) * 100;
                    document.getElementById('prep_progress').innerHTML = progression.toString();
                }

                fr.onload = function () {
                    data = fr.result;
                    avancement = 0;
                    taille = fr.result.byteLength;
                    if (taille > unMO) {
                        increment_avancement = unMO;
                    }
                    else {
                        increment_avancement = taille;
                    }
                    tl_taille.innerHTML =  (Math.round(taille / 1024)).toString();
                    avancement = increment_avancement;
                    taille -= increment_avancement;

                    socket.emit('televersement_fichier', { file: fichier.name, octet: data.slice(0, avancement) });
                }

                // Il faut préparer les listener avant d'appeler la fonction de lecture de fichier
                fr.readAsArrayBuffer(fichier);
            }
        }
    });

    socket.on('lancement_analyse', function(message){
        info_archive.innerHTML = message;
        execution_prog_attente.style.display = "block";
    });

    socket.on('preparation_archive', function(message){
        info_archive.innerHTML = message;
        execution_prog_attente.style.display = "none";
        zip_chargement.style.display = "table";
    });

    socket.on('erreur_analyse', function (erreur) {
        execution_prog_attente.style.display = "none";
        zip_chargement.style.display = "none";
        info_archive.innerHTML = erreur;
    })

    socket.on('lien_telechargement', function (lien) {
        info_archive.innerHTML = "Archive créée"
        zip_chargement.style.display = "none";
        download_archive.style.display = "block";
        download_archive.innerHTML = "<a id=download_archive_link href='" + lien + "' download>Télécharger l'archive</a>"
    });

    socket.on('console_message', function (data) {
        if (console_debug.style.display == "") {
            console_debug.style.display = "block";
        }
        console_debug.innerHTML = console_debug.innerHTML + data + "\n";
        console_debug.scrollTop = console_debug.scrollHeight;
    });
}


window.onload = main;
