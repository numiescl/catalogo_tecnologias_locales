const listadoTecnologias = document.getElementById('listado-tecnologias')
const form = document.getElementById('search-form')
const csrf = document.getElementsByName('csrfmiddlewaretoken')
const searchQuery = document.getElementById('query')
const filtros = {}

function buscarTodas() {
    fetch('/buscar-tecnologias')
        .then(response => {
            return response.text()
        })
        .then(html => {
            let parser = new DOMParser()
            let doc = parser.parseFromString(html, 'text/html')
            listadoTecnologias.innerHTML = doc.body.innerHTML
        }).catch(error => {
        console.warn('Error.', error)
    })
    filtros.zona = []
    filtros.categoria = []
    filtros.territorio = []

    document.querySelectorAll('.activo')
    .forEach(boton => {
        boton.classList.remove('activo')
    })
    document.getElementById('query').value=""
}

form.addEventListener('submit', event => {
    event.preventDefault()

    let data = new FormData()
    data.append('query', searchQuery.value)

    fetch('/buscar-tecnologias', {
        method: 'POST',
        body: data,
        headers: {
            'X-CSRFToken': csrf[0].value
        }
    }).then(response => {
        return response.text()
    }).then(html => {
        let parser = new DOMParser()
        let doc = parser.parseFromString(html, 'text/html')
        listadoTecnologias.innerHTML = doc.body.innerHTML
    }).catch(error => {
        console.warn('Error.', error)
    })
})

function toggle(array, value) {
    let index = array.indexOf(value)

    if (index === -1) {
        array.push(value)
    } else {
        array.splice(index,1)
    }
}

function filtrarPorEtiqueta(etiqueta, value) {

    document.querySelector(`[value="${value}"]`).classList.toggle("activo")

    toggle(filtros[etiqueta], value)

    let data = new FormData()
    data.append('query', query.value)

    if (filtros.zona.length > 0) {
        data.append('zona', filtros.zona)
    }

    if (filtros.categoria.length > 0) {
        data.append('categoria', filtros.categoria)
    }

    if (filtros.territorio.length > 0) {
        data.append('territorio', filtros.territorio)
    }

    fetch('buscar-tecnologias', {
        method: 'POST',
        body: data,
        headers: {
            'X-CSRFToken': csrf[0].value
        }
    }).then(response => {
        return response.text()
    }).then(html => {
        let parser = new DOMParser()
        let doc = parser.parseFromString(html, 'text/html')
        listadoTecnologias.innerHTML = doc.body.innerHTML
    }).catch(error => {
        console.warn('Error.', error)
    })
}

buscarTodas()