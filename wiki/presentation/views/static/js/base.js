'use strict'


let IndicatorButton = function(selector) {
    this.selector = selector
    this.timerId = null
}

IndicatorButton.prototype.state = function(state) {
    $(this.selector).removeClass('waiting loading done fail').addClass(state)
    if(state == 'done' || state == 'fail') {
        if(this.timerId)
            clearTimeout(this.timerId)
        this.timerId = setTimeout(() => this.state('waiting'), 2000)
    }
}


$(function() {
    $('#login-menu-view').on('click', () => {
        location.href = '?'
    })
    $('#login-menu-edit').on('click', () => {
        location.href = '?edit=1'
    })
    $('#login-menu-logout').on('click', () => {
        $.ajax({
            cache: false,
            method: 'POST',
            url: '/api/logout'
        }).done((_) => {
            location.href = '?'
            document.cookie = 'session_id=_'
        })
    })

    let source = $('#markdown-source').text()
    if(source) {
        $('#markdown-preview').html(marked(source))
        document.querySelectorAll('pre code').forEach((block) => {
            hljs.highlightBlock(block)
        })
    }

    let EditButton = new IndicatorButton('#edit-submit')
    let EditView = Vue.createApp({
        delimiters: ['[[', ']]'],
        data: function() {
            return {
                markedJsTimer: null,
                codeMirror: null,
                page: {
                    page_id: '',
                    title: '',
                    body: '',
                    lastmodified: 0,
                    version: 0
                }
            }
        },
        mounted: function() {
            this.getPage()
        },
        methods: {
            updateMarkdownPreview: function() {
                $('#markdown-preview').html(marked(this.codeMirror.getValue()))
                document.querySelectorAll('pre code').forEach((block) => {
                    hljs.highlightBlock(block)
                })
            },
            updateMarkdownPreviewDelay: function() {
                if(this.markedJsTimer)
                    clearTimeout(this.markedJsTimer)
                this.markedJsTimer = setTimeout(() => {
                    this.updateMarkdownPreview()
                    this.markedJsTimer = null
                }, 1000)
            },
            getPage: function() {
                $.ajax({
                    cache: false,
                    method: 'GET',
                    url: '/api/page' + new URL(location.href).pathname
                }).done((response) => {
                    let editor = $('#markdown-editor').text(response.body)
                    this.page = response
                    this.codeMirror = CodeMirror.fromTextArea(editor[0], {
                        mode: 'markdown',
                        theme: 'paraiso-dark',
                        autoFocus: true,
                        lineNumbers: true,
                        lineWrapping: true,
                        smartIndent: true
                    })
                    this.codeMirror.on('changes', this.updateMarkdownPreviewDelay)
                    this.updateMarkdownPreview()
                })
            },
            editButtonClick: function() {
                EditButton.state('loading')
                $.ajax({
                    cache: false,
                    method: 'POST',
                    url: '/api/page/' + this.page.page_id,
                    data: {
                        title: this.page.title,
                        body: this.codeMirror.getValue(),
                        version: this.page.version,
                    }
                }).done((response) => {
                    this.page = response
                    $('#page-version').val(response.version)
                    EditButton.state('done')
                }).fail(() => {
                    EditButton.state('fail')
                })
            }
        }
    }).mount('#edit')

    let LoginButton = new IndicatorButton('#login-button')
    let LoginView = Vue.createApp({
        delimiters: ['[[', ']]'],
        data: function() {
            return {
                user_id: '',
                password: ''
            }
        },
        methods: {
            loginButtonClick: function() {
                LoginButton.state('loading')
                $.ajax({
                    cache: false,
                    method: 'POST',
                    url: '/api/login',
                    data: {
                        password: this.password
                    }
                }).done((response, textStatus, jqXHR) => {
                    let date = new Date(response.expires * 1000)
                    document.cookie = 'session_id=' + response.session_id + ';expires=' + date.toUTCString();
                    location.href = '/'
                    LoginButton.state('done')
                }).fail((jqXHR, textStatus, errorThrown) => {
                    LoginButton.state('fail')
                })
            }
        }
    }).mount('#login')
})
