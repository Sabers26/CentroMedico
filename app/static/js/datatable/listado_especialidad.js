let dataTable;
let dataTableIsInitialized;

const dataTableOptions = {
    columnDefs: [
        { className: "centered", targets: [0, 1] },
        { orderable: false, targets: [0, 1] },
        { searchable: true, targets: [0, 1] },
    ],
    pageLength: 4,
    destroy: true,
    language: {
        url: '//cdn.datatables.net/plug-ins/1.13.4/i18n/es-ES.json',
    },
    initComplete: function () {
        this.api().columns([0,1]).every(function () {
            let column = this;
    
            // Create select element
            let select = document.createElement('select');
            select.className = "form-select form-select-sm";
            select.add(new Option(''));
            column.header().replaceChildren(select);
    
            // Apply listener for user change in value
            select.addEventListener('change', function () {
                var val = DataTable.util.escapeRegex(select.value);
    
                column
                    .search(val ? '^' + val + '$' : '', true, false)
                    .draw();
            });
    
            // Add list of options
            column
                .data()
                .unique()
                .sort()
                .each(function (d, j) {
                    select.add(new Option(d));
                });
        });
    }
};

const initDataTable = async () => {
    if (dataTableIsInitialized) {
        dataTable.destroy();
    }

    await listausu();

    // Inicializa los DataTables solo si no está ya inicializado
    if (!dataTableIsInitialized) {
        dataTable = $("#datatable-responsive").DataTable(dataTableOptions);
        dataTableIsInitialized = true;
    }

    // Agrega los selects para filtrar en la fila de filtro
    dataTable.columns().every(function () {
        let column = this;
        let select = $('<select><option value=""></option></select>')
            .appendTo($(column.header()).empty())
            .on('change', function () {
                let val = $.fn.dataTable.util.escapeRegex($(this).val());
                column.search(val ? '^' + val + '$' : '', true, false).draw();
            });

        column.data().unique().sort().each(function (d, j) {
            select.append('<option value="' + d + '">' + d + '</option>');
        });
    });
};

const listausu = async () => {
    console.log("listausu se está ejecutando");
    try {
        console.log("INFORMACAOOOOOO")
        const data = horas
        const rut = rut_paciente

        console.log(data)

        let content = ``;
        data.forEach((hora) => {
            console.log(hora[2]['fecha_horario'])
            content += `
                <tr>
                    <td>${hora[2]['fecha_horario']}</td>
                    <td>${hora[2]['horario']}</td>
                    <td>${hora[1]}</td>
                    <td><a href="#" onclick="tomar_atencion('${hora[0].replace("-", "")}', '${hora[2]['fecha_horario']}', '${hora[2]['id_horario']}')" role="button" class="btn btn-primary text-light">Tomar atencion</a></td>
                </tr>`;
        });
        $("#table_body_clientes").html(content);

    } catch (ex) {
        alert(ex);
    }
};

window.addEventListener('load', async () => {
    await initDataTable();
});