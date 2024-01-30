let tableIdInput = document.getElementById('table_id'); // Assurez-vous que l'ID correspond à celui dans votre HTML

let tables = document.querySelectorAll('.table21, .table22, .table41, .table11, .table12, .table13, .table14, .table15');

tables.forEach(table => {
    table.addEventListener('click', function() {
        this.classList.toggle('selected');

        tables.forEach(tbl => {
            if (tbl.classList.contains('selected')) {
                let tableId = tbl.getAttribute('data-table-id');
                tableIdInput.value = tableId;
            }
        });
    });
});
