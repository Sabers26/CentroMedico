let dataTable;
let dataTableIsInitialized;

const dataTableOptions = {
    columnDefs: [
        { className: "centered", targets: [0, 1, 2, 3] },
        { orderable: false, targets: [0, 1, 2, 3] },
        { searchable: true, targets: [0, 1, 2] },
    ],
    pageLength: 4,
    destroy: true,
    language: {
        url: '//cdn.datatables.net/plug-ins/1.13.4/i18n/es-ES.json',
    },
    initComplete: function () {
        this.api().columns([0,1, 2]).every(function () {
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
    try {
        const user = usuario;
        const data = datosUsuarios;
        console.log(data)
        let content = ``;

        if (data.length > 0) {
            data.forEach((atencion) => {
                // if (horario.disponible == "True") {
                //     horario.disponible = "Disponible";
                // } else {
                //     horario.disponible = "No Disponible";
                // }

                // horario.fecha_horario = convertirFormatoFecha(horario.fecha_horario);
                content += `
                <tr>
                    <td>${atencion.fecha_consulta}</td>
                    <td>${atencion.horario}</td>
                    <td>${atencion.finalizado}</td>
                    <td>${atencion.medico}</td>
                    <td>${atencion.costo}</td>
                    ${atencion.finalizado === "PENDIENTE" ?
                    '<td><a href="#" onclick="eliminar_atencion(\'' + atencion.id_atencion + '\', \'' + atencion.rut_medico + '\', \'' + atencion.fecha_atencion + '\',\'' + atencion.id_horario + '\',\'' + user + '\')" role="button" class="btn btn-primary text-light">DESHABILITAR</a></td>' :
                    '<td> </td>'
                }
                </tr>`;
            });
            $("#table_body_clientes").html(content);
        } else {

        }

    } catch (ex) {
        alert(ex);
    }
};

window.addEventListener('load', async () => {
    await initDataTable();
});


function convertirFormatoFecha(fechaString) {
    // Crear un objeto Date a partir de la cadena de fecha
    var fecha = new Date(fechaString);

    // Obtener los componentes de la fecha
    var dia = fecha.getDate();
    var mes = fecha.getMonth() + 1; // Meses en JavaScript son de 0 a 11
    var año = fecha.getFullYear();

    // Formatear la fecha en el formato deseado
    var formatoFecha = dia + '-' + mes + '-' + año;

    return formatoFecha;
}