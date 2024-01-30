// Sélectionnez le bouton en utilisant son ID
var submitButton = document.getElementById('submit');

// Ajoutez un gestionnaire d'événements pour le bouton
submitButton.addEventListener('click', function(event) { // Include event as an argument
    // Insérez ici le code à exécuter lorsque le bouton est cliqué
    var tableSelected = document.querySelector('.table21.selected, .table22.selected, .table41.selected, .table11.selected, .table12.selected, .table13.selected, .table14.selected, .table15.selected') !== null;

    // Select the name and date fields and get their values
    var name = document.getElementById('name').value;
    var date = document.getElementById('date').value;

    // Si tous les champs du formulaire sont remplis et une table a été sélectionnée
    if (name && date && tableSelected) {
        alert('Demande de réservation envoyée !');
        // Le formulaire peut être soumis
    } else {
        // Sinon, empêcher la soumission du formulaire
        event.preventDefault();
        alert('Veuillez remplir tous les champs du formulaire et sélectionner une table.');
    }
});

// Sélectionnez le champ de date en utilisant son ID
var dateField = document.getElementById('date');

// Ajoutez un gestionnaire d'événements pour le champ de date
dateField.addEventListener('change', function() {
    // Enregistrez la valeur de la date dans le localStorage
    localStorage.setItem('date', this.value);

    // Actualisez la page
    location.reload();
});

// Après le rechargement de la page, récupérez la valeur de la date du localStorage et rétablissez-la
window.onload = function() {
    var savedDate = localStorage.getItem('date');
    if (savedDate) {
        dateField.value = savedDate;
    }
};