$('.view_assertion').on('click', function() {
    const assertion_id = $(this).data('assertion-id');
    fetch(`/api/assertion/${assertion_id}`)
        .then(response => response.json())
        .then(data => {
            $('#modal .modal-body').text(JSON.stringify(data.content, null, 2));
            $('#modal').modal('show');
        });
    return false;
});