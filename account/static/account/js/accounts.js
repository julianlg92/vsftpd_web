$(document).ready(function () {
    let table = $('#user-table')

    table.DataTable({
        'processing': true,
        "columnDefs": [{ "width": "10%", "targets": 3 }, {className: 'text-center'}, 'targets: [0,1,2]'],
        'serverSide': false,
        'initComplete': function (settings) {

            // Update User
            $('#modal-user').on('submit', '.js-user-update-form', saveFrom);
            $('.js-update-user').click(loadForm);
            //
            // // Delete User
            $('#modal-user').on('submit', '.js-user-delete-form', saveFrom);
            $('.js-delete-user').click(loadForm);
        },
        ajax: {
            url: table.attr('data-url'),
            dataSrc: 'data',
        },
        columns: [
            {data: 'id'},
            {data: 'username'},
            {data: 'label'},
            {
                data: 'pk',
                className: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return `<div class="btn-group" role="group" aria-label="Actions">
                <button type="button" class="btn btn-outline-success js-update-user"
                        data-url="account/${data}/edit"><i
                        class="fa fa-user-edit"></i>
                </button>
                <button type="button" class="btn btn-outline-danger js-delete-user"
                        data-url="account/${data}/delete">
                        <i class="fa fa-trash"></i>
                </button>
            </div>`;
                }
            }
        ]
    });
    /* Functions */

    let loadForm = function () {
        let btn = $(this);
        $.ajax({
            url: btn.attr('data-url'),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $('#modal-user').modal('show');
            },
            success: function (data) {
                $('#modal-user .modal-content').html(data.html_form);
            },
        });
    };

    let saveFrom = function () {
        let form = $(this);
        $.ajax({
            url: form.attr('action'),
            data: form.serialize(),
            type: form.attr('method'),
            dataType: 'json',
            success: function (data) {
                if (data.form_is_valid) {
                    // $('#user-table tbody').html(data.html_user_list);
                    $('#modal-user').modal('hide');
                    let tab = $('#user-table').DataTable();
                    tab.ajax.reload();
                } else {
                    $('#modal-user .modal-content').html(data.html_form)
                }
            }
        });
        return false;
    };

    /*  Binding  */

// Create User
    $('.js-create-user').click(loadForm);
    $('#modal-user').on('submit', '.js-user-create-form', saveFrom);


});


