$('table.assertion-table tbody tr').on('click', function() {
    const assertion_uuid = $(this).data('assertion-uuid');
    const assertion_generator_uuid = $(this).data('assertion-generator-uuid');

    fetch(`/api/1/assertion/${assertion_uuid}`)
        .then(response => response.json())
        .then(data => {
            $('#modal .modal-title').text('Assertion Details');
            $('#modal .modal-body').text(JSON.stringify(data.content, null, 2));
            $('#modal .modal-body').addClass('monospace');
            $('#modal .modal-body').css('max-height', $(window).height() * 0.80);
            $('#modal .modal-footer .assertion-download').attr('href', '/assertions/' + assertion_uuid + '/download');
            $('#modal .modal-footer .assertion-more-info').data('assertion-generator-uuid', assertion_generator_uuid);
            $('#modal .modal-footer .assertion-more-info').show();
            $('#modal .modal-footer .assertion-download').show();
            $('#modal').modal('show');
        });

    return false;
});

$('table.policy-evaluation-result-table tbody tr').on('click', function() {
    const policy_uuid = $(this).data('policy-uuid');
    fetch('/api/1/help?' + new URLSearchParams({
        'type': 'policy',
        'policy_uuid': policy_uuid
    }))
    .then(response => response.text())
    .then(data => {
        if (!data) {
            data = 'Sorry, no help information is available.';
        }
        $('#modal .modal-body').html(data);
        $('#modal .modal-footer .assertion-more-info').hide();
        $('#modal .modal-footer .assertion-download').hide();
        $('#modal .modal-body').removeClass('monospace');
        $('#modal .modal-title').text('Policy Details');
        $('#modal .modal-body').css('max-height', $(window).height() * 0.80);
        $('#modal').modal('show');
    });
});

$('.assertion-more-info').on('click', function() {
    const assertion_generator_uuid = $(this).data('assertion-generator-uuid');

    fetch('/api/1/help?' + new URLSearchParams({
        'type': 'assertion_generator',
        'assertion_generator_uuid': assertion_generator_uuid
    }))
    .then(response => response.text())
    .then(data => {
        if (!data) {
            data = 'Sorry, no help information is available.';
        }
        $('#modal .modal-title').text('Assertion Info');
        $('#modal .modal-body').html(data);
        $('#modal .modal-body').removeClass('monospace');
        $('#modal .modal-body').css('max-height', $(window).height() * 0.80);
        $('#modal .modal-footer .assertion-more-info').hide();
        $('#modal .modal-footer .assertion-download').hide();
        $('#modal').modal('show');
    });
});

$('.policy_help').on('click', function() {
    fetch('/api/1/policy/help?' + new URLSearchParams({
        'target': 'policy',
        'uuid': $(this).data('policy-uuid')
    }))
    .then(response => response.text())
    .then(data => {
        if (!data) {
            data = 'Sorry, no help information is available.';
        }
        $('#modal .modal-body').html(data);
        $('#modal .modal-footer .assertion-more-info').hide();
        $('#modal .modal-footer .assertion-download').hide();
        $('#modal .modal-body').removeClass('monospace');
        $('#modal .modal-title').text('Assertion Info');
        $('#modal .modal-body').css('max-height', $(window).height() * 0.80);
        $('#modal').modal('show');
    });
});

