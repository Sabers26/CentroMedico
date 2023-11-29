let dataTable;
let dataTableIsInitialized;

const dataTableOptions = {
    columnDefs: [
        { className: "centered", targets: [0, 1, 2] },
        { orderable: true, targets: [0, 1, 2] },
        { searchable: true, targets: [0, 1, 2] },
    ],
    pageLength: 4,
    destroy: true,
    language: {
        url: '//cdn.datatables.net/plug-ins/1.13.4/i18n/es-ES.json',
    },
    initComplete: function () {
        this.api().columns().every(function () {
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
        const response = await fetch("http://127.0.0.1:8000/lista_usuarios")
        const data = await response.json();

        let content = ``;
        data.forEach((usuario) => {
            content += `
                <tr>
                    <td>${usuario.rut_usuario}</td>
                    <td>${usuario.nombre_usuario}</td>
                    <td>${usuario.nombre_tipo}</td>
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