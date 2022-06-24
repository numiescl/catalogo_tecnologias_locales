document.addEventListener('DOMContentLoaded', function () {
    const shareButton = getAll('.share-btn')
    // Share API
    const titulo = document.querySelector('h1').innerHTML
    const texto = "Encontré esta tecnología en el Catálogo de Tecnologías Locales."

    shareButton.forEach(function (el) {
        el.addEventListener('click', () =>{
            if (navigator.share) {
                navigator.share({
                    title: titulo,
                    text: texto,
                    url: window.location.href
                }).then(() => {
                    console.log('shared')
                }).catch(err => {
                    console.log('Algo pasó', err.message)
                })
            } else {
                let target = el.dataset.target;
                let $target = document.getElementById(target);
                rootEl.classList.add('is-clipped');
                $target.classList.add('is-active');
            }
        })
    })

    // Modals
    let rootEl = document.documentElement;
    let $modals = getAll('.modal');
    let $modalCloses = getAll('.modal-background, .modal-close, .modal-card-head .delete, .modal-card-foot .button');
    if ($modalCloses.length > 0) {
        $modalCloses.forEach(function ($el) {
            $el.addEventListener('click', function () {
                closeModals();
            });
        });
    }
    document.addEventListener('keydown', function (event) {
        var e = event || window.event;
        if (e.keyCode === 27) {
            closeModals();
        }
    });
    function closeModals() {
        rootEl.classList.remove('is-clipped');
        $modals.forEach(function ($el) {
            $el.classList.remove('is-active');
        });
    }
    // Functions
    function getAll(selector) {
        return Array.prototype.slice.call(document.querySelectorAll(selector), 0);
    }
});


