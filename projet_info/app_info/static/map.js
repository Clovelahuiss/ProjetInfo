let tables = document.querySelectorAll('.table21, .table22, .table41, .table11, .table12, .table13, .table14, .table15');
let tableIdInput = document.getElementById('table_id');

tables.forEach(table => {
    table.addEventListener('click', function() {
        // Désélectionner toutes les tables et sélectionner celle-ci
        tables.forEach(tbl => tbl.classList.remove('selected'));
        this.classList.add('selected');

        // Mettre à jour la valeur du champ caché avec l'ID de la table
        tableIdInput.value = this.getAttribute('data-table-id');
    });
});