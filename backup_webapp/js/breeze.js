host = window.location.host
app_path = '/backup_app'
app_url = '//' + host + '' + app_path

// start app
get_path = window.location.pathname
tmp = get_path.split("/")
page = tmp[tmp.length-1]
if(page == 'home.html') {
    $('document').ready(function() {
        check_login()
    })
}


function try_access() {

    password = $('[lgn-pswd]').val()

    if(password == "") {
        $('[lgn-pswd]').addClass('is-danger')
        $('[lgn-pswd]').addClass('is-focused')
        return
    } else {
        $('[lgn-pswd]').removeClass('is-danger')
        $('[lgn-pswd]').removeClass('is-focused')

        $.ajax({
            url: app_url + '/login',
            method: 'POST',
            data: {
                'password' : password
            },
            success: function(data) {
                if(data['code'] == 200) {

                    localStorage.setItem('user_token',data['token'])
                    window.location = 'home.html'

                } else {
                    notify({
                        'code' : 403,
                        'message' : 'Acesso negado!'
                    })    
                }
            },
            timeout:10000,
            error: function(a,b,c) {
                notify({
                    'code' : 500,
                    'message' : c
                })
            }
        })

    }

}

function check_login() {

    token = localStorage.getItem('user_token')
    
    $.ajax({
        url: app_url + '/login/check',
        method: 'POST',
        data: {
            'token' : token
        },
        success: function(data) {
            
            if(data['code'] != 200) {
                window.location = 'index.html'
            } else {
                startApp()
            }
        },
        timeout:10000,
        error: function(a,b,c) {
            notify({
                'code' : 500,
                'message' : c
            })
        }
    })
}

function startApp() {
    console.log("START APP!!!")
    list_backups()
}

// List backups
function list_backups() {
    
    token = localStorage.getItem('user_token')
    
    $.ajax({
        url: app_url + '/backup/list',
        method: 'POST',
        beforeSend: function() {
            $(".carregando").show()
        },
        data: {
            'token' : token
        },
        success: function(data) {
            
            if(data['code'] == 200) {
                list = ""

                if(data['data'].length == 0) {
                    $('.app').append('<div empty-message style="text-align:center">Nenhum backup encontrado.</div>')
                    $("#dump-list").hide()
                    return
                } else {
                    $("#dump-list").show()
                    $("[empty-message]").hide()
                }

                for(l in data['data']) {

                    
                    dump_mtime = data['data'][l]['file_mtime']
                    dump_name = data['data'][l]['file_name']
                    dump_size = data['data'][l]['file_size']

                    btn_actions = '<div class="buttons are-small" style="float:right">'
                    btn_actions = btn_actions.concat(`<button class="button is-link" onclick="restore_backup('${dump_name}')" >Restaurar</button>`)
                    btn_actions = btn_actions.concat(`<button class="button is-danger" onclick="delete_backup('${dump_name}')">Remover</button>`)
                    btn_actions = btn_actions.concat('</div>')

                    list = list.concat('<tr>')
                    list = list.concat('<td>' +dump_mtime+ '</td>')
                    list = list.concat('<td>' +dump_name+ '</td>')
                    list = list.concat('<td>' +dump_size+ '</td>')
                    list = list.concat('<td>' +btn_actions +'</td>')
                    list = list.concat('</tr>')
                }

                $('#dump-list > tbody').html(list)

            } else {
                notify({
                    'code' : 500,
                    'message' : data['message']
                })
            }

        },
        timeout:10000,
        error: function(a,b,c) {
            notify({
                'code' : 500,
                'message' : c
            })
        },
        complete: function() {
            $(".carregando").hide()
        }
    })
}

function delete_backup(f) {
    d = {
        'data' : f,
        'function' : 'delete_backup_confirm'
    }
    question({
        'title' : 'Remover backup',
        'message' : 'Tem certeza que deseja remover o backup selecionado?',
        'call' : d,
        'type' : 'danger'
    })
}



function create_backup() {
    d = {
        'data' : '',
        'function' : 'create_backup_confirm'
    }
    question({
        'title' : 'Criar backup',
        'message' : 'Deseja criar um backup do Banco de dados do Netbox?',
        'call' : d,
        'type' : ''
    })
}
function delete_backup_confirm(f) {
        
    $.ajax({
        url: app_url + '/backup/remove',
        method: 'POST',
        data: {
            'token' : token,
            'file' :  f
        },
        beforeSend: function() {
            $(".carregando").show()
        },
        success: function(data) {
            
            if(data['code'] == 200) {
                notify({
                    'code' : 200,
                    'message' : 'Backup removido com sucesso!'
                })

                list_backups()

            } else {
                notify({
                    'code' : 500,
                    'message' : 'Erro ao remover o backup'
                })
            }
        },
        timeout: 10000,
        error:function(a,b,c) {
            notify({
                'code' : 500,
                'message' : c
            })
        },
        complete: function() {
            $(".carregando").hide()
        }
    })
}

function create_backup_confirm() {
    
    token = localStorage.getItem('user_token')
    
    $.ajax({
        url: app_url + '/backup/create',
        method: 'POST',
        data: {
            'token' : token
        },
        beforeSend: function() {
            $(".carregando").show()
        },
        success: function(data) {
            
            if(data['code'] == 200) {
                notify({
                    'code' : 200,
                    'message' : 'Backup criado com sucesso!'
                })

                list_backups()

            } else {
                notify({
                    'code' : 500,
                    'message' : data['message']
                })
            }
        },
        timeout: 10000,
        error:function(a,b,c) {
            notify({
                'code' : 500,
                'message' : c
            })
        },
        complete: function() {
            $(".carregando").hide()
        }
    })
}

// Restore backup
function restore_backup(f) {
    d = {
        'data' : f,
        'function' : 'restore_backup_confirm'
    }
    question({
        'title' : 'Restaurar um backup',
        'message' : 'Deseja restaurar o backup selecionado?',
        'call' : d,
        'type' : ''
    })
}
function restore_backup_confirm(d) {

    $.ajax({
        url: app_url + '/backup/restore',
        method: 'POST',
        data: {
            'token' : token,
            'file' :  d
        },
        beforeSend: function() {
            $(".carregando").show()
        },
        success: function(data) {
            console.log(data)
            if(data['code'] == 200) {
                notify({
                    'code' : 200,
                    'message' : 'Backup restaurado com sucesso!'
                })

                list_backups()

            } else {
                notify({
                    'code' : 500,
                    'message' : 'Erro ao restaurar o backup'
                })
            }
        },
        timeout: 10000,
        error:function(a,b,c) {
            notify({
                'code' : 500,
                'message' : c
            })
        },
        complete: function() {
            $(".carregando").hide()
        }
    })



}


function notify(d) {

    code = d['code']

    if(code >= 100 && code < 200) {
        type = 'is-info'
    } else if(code >= 200 && code < 300) {
        type = 'is-success'
    } else if(code >= 300 && code < 400) {
        type = ''
    } else if(code >= 400 && code < 600) {
        type = 'is-danger'
    }

    message = `<article class="message ${type} " style="margin-top:20px">`
    message = message.concat('<div class="message-body">')
    message = message.concat(d['message'])
    message = message.concat('</div>')
    message = message.concat('</article>')

    $(".notify").html(message)
    setTimeout(function() {
        $(".notify > article").hide()
    },10000)

}


$('.app > .menu > ul > li > a').click(function() {
    $( this ).closest('ul').find('a').removeClass('active')
    $( this ).addClass('active')
})

/* Modal */
function question(d) {

    // get modal dynamic data
    title = d['title']
    message = d['message']
    call = d['call']
    type = d['type']

    // type button
    if( type == 'danger') {
        button_class = 'is-danger'
    } else {
        button_class = 'is-link'
    }

    // Remove question modal id exists
    $('.modal').remove()

    // Add modal
    modal = ''    
    modal = modal.concat('<div class="modal is-active">')
    modal = modal.concat('<div class="modal-background"></div>')
    modal = modal.concat('<div class="modal-card">')
    modal = modal.concat('<header class="modal-card-head">')
    modal = modal.concat('<p class="modal-card-title is-size-4"><span class="is-size-5">' + title + '</span></p>')
    modal = modal.concat('<button class="delete" aria-label="close" onclick="close_modal()"></button>')
    modal = modal.concat('</header>')
    modal = modal.concat('<section class="modal-card-body">')
    modal = modal.concat(message)
    modal = modal.concat('</section>')
    modal = modal.concat('<footer class="modal-card-foot">')
    modal = modal.concat('<button class="button is-small '+ button_class +'" onclick="modal_confirm(call)">Confirmar</button>')
    modal = modal.concat('<button class="button is-small" onclick="close_modal()">Cancelar</button>')
    modal = modal.concat('</footer>')
    modal = modal.concat('</div>')
    modal = modal.concat('</div>')

    //$('HTML').addClass('is-clipped')
    $('BODY').append(modal)

}

function modal_confirm(d) {
    
    func = d['function']
    data = d['data']
    window[func](data);
    close_modal()
}

function close_modal() {
    $(".modal").remove()
}