$(function() {

    'use strict';

    // Form

    var contactForm = function() {

        if ($('#contactForm').length > 0) {
            $("#contactForm").validate({
                rules: {
                    fichier: "required",
                    pretrainedModels: "required",
                    classification: "required",
                },
                messages: {
                    fichier: "Veuillez selectionner un fichier Diff",
                    pretrainedModels: "Veuillez sélectionner un modèle pour l'apprentissage des caractéristiques",
                    classification: "Veuillez sélectionner un algorithme de classification"
                },
            });
        }
    };
    contactForm();

});