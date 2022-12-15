$(document).ready(function () {
    /* Initialize Bootstrap Components */
    $('[data-toggle="popover"]').popover();
    $('[data-toggle="tooltip"]').tooltip();

    /* Add CSRF token to AJAX requests */
    $.ajaxSetup({
        'timeout': 15000,
        'beforeSend': function (jqXHR, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type) && !this.crossDomain) {
                jqXHR.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        }
    });

    /*
     * Initialize the DataTable (finding list)
     */
    $('#finding_list').DataTable({
        select: {
            style: 'os',
            info: false
        },
        scrollResize: true,
        scrollCollapse: true,
        scrollY: '100',
        lengthChange: false,
        paging: false,
        info: false,
        searching: false,
        order: [
            [0, 'asc'],
            [1, 'asc']
        ],
        columnDefs: [
            { 'searchable': false, 'targets': [] },
        ],
        initComplete: function (settings, json) {
            $('#finding_list').on('select.dt', function (e, dt, type, indexes) {
                if (type === 'row' && indexes.length === 1) {
                    let row = $('#finding_list').DataTable().rows(indexes).nodes().to$();
                    let finding_uuid = row.data('finding-uuid');
                    document.location.href = `/findings/${finding_uuid}`;
                }
            });
        }
    });

    // Initialize the ACE editor
    initialize_editor();

    // Auto-open single-child nodes
    $("#data").on("open_node.jstree", function (e, data) {
        try {
            if (data.node.children.length == 1) {
                $('#data').jstree().open_node(data.node.children[0])
            }
        } catch (e) {
            console.log(`Error: ${e}`);
        }
    });
})

// General Purpose Helper Functions
let getCookie = function (name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const load_source_code = function(options) {
    $('#finding_center').css('opacity', '0.20');
    $.ajax({
        'url': '/api/findings/get_source_code',
        'method': 'GET',
        'data': {
            'file_uuid': options['file_uuid']
        },
        'dataType': 'json',
        'success': function ({ file_contents, file_name, status }, textStatus, jqXHR) {
            let editor = ace.edit("editor");
            editor.getSession().setValue(atob(file_contents));
            var get_mode_filename = (file_name) => {
                if (file_name.indexOf('.sarif')) {
                    return `${file_name}.json`;
                }
                return file_name;
            }
            let mode = ace.require("ace/ext/modelist").getModeForPath(get_mode_filename(file_name)).mode;
            editor.session.setMode(mode);
            editor.resize();
            // Show the editor if needed
            $('#editor-container').removeClass('d-none');

            // Set the editor title
            const file_line = $(document.body).data('current_finding').file_line;
            if (file_line !== undefined && options['first'] === true) {
                $('#file_path').text(file_name + ":" + file_line);
            } else {
                $('#file_path').text(file_name);
            }

            //var path_abbrev = path;
            //if (path_abbrev.length > 150) {
            //    path_abbrev = '...' + path_abbrev.substring(path_abbrev.length - 150, path_abbrev.length);
            //}
            //$('#editor-title .text').text(path_abbrev).attr('title', path);
            const file_path = $(document.body).data('current_finding').file_path;
            var finding_title = ($(document.body).data('current_finding').finding_title || '').substring(0, 40);
            if (file_path !== undefined && file_line !== undefined && options['first'] === true) {
                let session = ace.edit('editor').getSession();
                session.clearAnnotations();
                session.setAnnotations([{
                    row: file_line - 1,
                    column: 0,
                    text: finding_title,
                    type: 'error'
                }]);
            } else {
                ace.edit('editor').getSession().clearAnnotations();
            }

            $(window).trigger('resize');
            $('#editor').css('height', $(window).height() - $('#editor').offset().top - 10);

            if (options['first'] === true) {
                window.setTimeout(function() {
                    ace.edit('editor').scrollToLine(file_line, true, false);
                }, 50);
            }
        },
        'error': function (jqXHR, textStatus, errorThrown) {
            ace.edit('editor').getSession().clearAnnotations();
            ace.edit('editor').getSession().setMode('ace/mode/text')
            set_editor_text(`Error ${jqXHR.status}: ${jqXHR.responseJSON.message}.`);
        },
        'complete': function () {
            $('#finding_center').css('opacity', '1.0');
        }
    });
};
const initialize_editor = function () {
    try {
        let editor = ace.edit("editor"),
            session = editor.getSession();
        editor.setOptions({
            useWorker: false
        });
        editor.setShowPrintMargin(false);
        editor.setTheme("ace/theme/cobalt");
        editor.setReadOnly(true)
        editor.setOptions({
            'fontFamily': 'Inconsolata',
            'fontSize': localStorage.getItem('last-used-editor-font-size') || '1.1rem',
        });
    } catch (e) {
        console.log(e);
    }
}

const set_editor_text = function (text) {
    let editor = ace.edit("editor");
    editor.getSession().setValue(text);
    editor.resize();
}

const load_file_listing = function (options, callback) {
    $.ajax({
        'url': '/api/findings/get_files',
        'method': 'GET',
        'data': options,
        'success': function (data, textStatus, jqXHR) {
            if ($('#data').jstree(true)) {
                $('#data').jstree(true).destroy();
            }
            $('#data').jstree({
                'core': {
                    'data': data.data,
                    'multiple': false,
                    'themes': {
                        'dblclick_toggle': false,
                        'icons': true,
                        'name': 'proton',
                        'responsive': true
                    }
                },
                'animation': 40,
                'plugins': ['sort', 'contextmenu'],
                'sort': function (a, b) {
                    a1 = this.get_node(a);
                    b1 = this.get_node(b);
                    if (a1.children.length === 0 && b1.children.length === 0) {
                        return a1.text.localeCompare(b1.text);
                    } else if (a1.children.length === 0) {
                        return 1;
                    } else if (b1.children.length === 0) {
                        return -1;
                    } else {
                        return a1.text.localeCompare(b1.text);
                    }
                },
                'contextmenu': {
                    items: function (node) {
                        var tree = $('#data').jstree(true);
                        if (node.id == '#') {
                            return {};
                        }
                        return {
                            "Download": {
                                "separator_before": false,
                                "separator_after": false,
                                "label": "Download",
                                "icon": "fa fa-download",
                                "_class": "file_tree_context_menu_item",
                                "action": function (obj) {
                                    var node = tree.get_node(obj.reference);
                                    if (node.children.length === 0) {
                                        document.location.href = `/api/findings/download_file?file_uuid=${node.original.file_uuid}`;
                                    } else {
                                        //document.location.href = `/api/findings/download_file?finding_uuid=${options.finding_uuid}&file_path=${node.id}&recursive=true`;
                                        alert('not implemented');
                                    }
                                }
                            }
                        }
                    }
                }
            });
            $('#data').on({
                "loaded.jstree": function (event, data) {
                    $(this).jstree("open_node", $(this).find('li:first'));
                },
                "changed.jstree": function (event, data) {
                    if (data && data.node && data.node.children && data.node.children.length === 0) {
                        const original_file_uuid = $.data(document.body, 'current_finding').file_uuid;
                        if (data.node.original.file_uuid != original_file_uuid) {
                            $('#finding_center').removeClass('col-lg-8').addClass('col-lg-10');
                            $('#finding_right').remove();
                        }
                        load_source_code({
                            'file_uuid': data.node.original.file_uuid,
                            'first': data.event === undefined    // Event is undefined when changed is called manually upon paage load (@magic)
                        });
                    }
                }
            });
        }
    });
}

const beautify_source_code = () => {
    const beautify = ace.require("ace/ext/beautify");
    const editor = ace.edit("editor");
    if (!!beautify && !!editor) {
        beautify.beautify(editor.session);
    }
};

const toggle_word_wrap = () => {
    const session = ace.edit('editor').getSession();
    session.setUseWrapMode(!session.getUseWrapMode());
}

const change_font_size = (size) => {
    const editor = ace.edit('editor');
    let fontSize = editor.getFontSize();
    if (fontSize.indexOf('rem') > -1) {
        fontSize = fontSize.replace('rem', '');
        fontSize = parseFloat(fontSize) * size;
        fontSize = fontSize + 'rem';
    } else if (fontSize.indexOf('px') > -1) {
        fontSize = fontSize.replace('px', '');
        fontSize = parseFloat(fontSize) * size;
        fontSize = fontSize + 'px';
    }
    editor.setFontSize(fontSize);
    localStorage.setItem('last-used-editor-font-size', fontSize);
}

const IS_SUCCESS = (data) => {
    if (!data) return false;
    const status = data.status + '';
    if (status === 'success') return true;
    if (status === 'ok' || status.startsWith('ok')) return true;
    return false;
}