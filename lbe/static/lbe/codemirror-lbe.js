document.addEventListener('DOMContentLoaded', function (ev) {
    var textareas = document.getElementsByClassName('codemirror-widget'),
        textareasLength = textareas.length;
    for (var i = 0; i < textareasLength; i++) {
        CodeMirror.fromTextArea(textareas[i], {
            mode: 'gfm',
            indentunit: 4,
            tabSize: 4,
            indentWithTabs: false,
            lineWrapping: true
        })
    }
});
