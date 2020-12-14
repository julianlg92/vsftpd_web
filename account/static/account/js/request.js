$(document).ready(function () {
    let table = $('#disbled-table')

    table.DataTable({
        'processing': true,
        'ajax': {
            'url': table.attr('data-url'),
            'dataSrc': 'data',
        },
        'columns': [
            { data: 'id' },
            { data: 'username' },
            { data: 'label' },
            {
                data: 'pk',
                orderable: false,
                className: 'text-center',
                render: function (data, type, row) {
                    return `<div class="btn-group" role="group" aria-label="Actions">
                    <button type="button" class="btn btn-outline-success js-approve-user"
                            data-url="/account/${data}/enable/"><i
                            class="far fa-thumbs-up"></i>
                    </button>
                    <button type="button" class="btn btn-outline-danger js-disapprove-user"
                            data-url="/account/${data}/delete/">
                            <i class="far fa-thumbs-down"></i>
                    </button>
                </div>`;
                }
            }
        ]
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');

    const approveUser = function () {
        const btn = $(this);
        $.ajax({
            'url': btn.attr('data-url'),
            'type': 'put',
            'dataType': 'json',
            'headers': {"X-CSRFToken":csrftoken},
            'success': function (data) {
                if (data.success) {
                    Swal.fire({
                        icon: 'success',
                        title: 'Enabled',
                        text: `User ${data.username} is now enable`
                    });
                    const tab = $('#disbled-table').DataTable();
                    tab.ajax.reload();
                } else {
                    Swal.fire({
                        icon: 'error',
                        title: 'Opps...',
                        text: `Something went wrong`
                    });
                }
            },
        });
    };

    const deleteUser = function () {
        const btn = $(this);
        $.ajax({
            'url': btn.attr('data-url'),
            'type': 'post',
            'dataType': 'json',
            'headers': {"X-CSRFToken":csrftoken},
            'success': function (data) {
                if (data.form_is_valid) {
                    Swal.fire({
                        icon: 'success',
                        title: 'Deleted',
                        text: `User ${data.username}'s request has been remved`
                    });
                    const tab = $('#disbled-table').DataTable();
                    tab.ajax.reload();
                } else {
                    Swal.fire({
                        icon: 'error',
                        title: 'Opps...',
                        text: `Something went wrong`
                    });
                }
            },
        });
    };

    // Bindings
    let table_instance = $('#disbled-table').DataTable()

    // Approve
    table_instance.on('click', '.js-approve-user', approveUser)
    
    // Delete
    table_instance.on('click', '.js-disapprove-user', deleteUser)
});