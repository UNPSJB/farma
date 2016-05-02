function modalAjax(){ 
    var getElements = function() {
        this.$modalDetalles = $('#modal-ver-detalles');
        this.$modalRemitos = $('#modal-ver-remitos');
        this.$tableDetalles = this.$modalDetalles.find('table tbody');
        this.$tableRemitos = this.$modalRemitos.find('table tbody');
        this.$btnsVerDetalles = $('.action .btn-ver-detalles');
        this.$btnsVerRemitos = $('.action .btn-ver-remitos');
    },
    bindEvents = function() {
        this.$btnsVerDetalles.on('click', loadModalVerDetalles.bind(this));
        this.$btnsVerRemitos.on('click', loadModalVerRemitos.bind(this));
    },
    init = function() {
        getElements();
        bindEvents();
    },
    getData = function(fn, keyData) {
        $.ajax({
            type: 'GET',
            url: this.url,
            dataType: 'json',
            success: function(data){
                if(data) {
                    fn(data[keyData]);
                }
                
            },
            error: function(err){
                alert("Fallo Ajax");
            },
        });
    },
    loadModalVerDetalles = function(e) {
        this.url = $(e.target).data('url');
        getData(setDataDetalles, 'detalles');
    },
    loadModalVerRemitos = function(e) {
        this.url = $(e.target).data('url');
        getData(setDataRemitos, 'remitos');
    },
    setDataDetalles = function(detalles) {
        var rows = document.createDocumentFragment(),
        i, max;
        this.$tableDetalles.empty();

        for(i = 0, max = detalles.length; i < max; i+=1) {  
            var tr = document.createElement('tr'),
            medicamento = document.createElement('td'),
            cantidad = document.createElement('td'),
            txtMedicamento = document.createTextNode(detalles[i]['medicamento']['descripcion']),
            txtCantidad = document.createTextNode(detalles[i]['cantidad']);

            medicamento.appendChild(txtMedicamento);
            cantidad.appendChild(txtCantidad);
            tr.appendChild(medicamento);
            tr.appendChild(cantidad);

            rows.appendChild(tr);
        }

        $tableDetalles.append(rows);
        this.$modalDetalles.modal('show');
    },
    setDataRemitos = function(remitos) {
        var rows = document.createDocumentFragment(),
        i, max;
        $tableRemitos.empty();
        if (remitos.length > 0) {
            this.$modalRemitos.find('.mensaje-sin-remitos').addClass('hidden');
            this.$tableRemitos.parent().removeClass('hidden');
            for(i = 0, max = remitos.length; i < max; i+=1) {  
                var tr = document.createElement('tr'),
                nroRemito = document.createElement('td'),
                fecha = document.createElement('td'),
                pdf = document.createElement('td'),
                linkPdf = document.createElement('a'),
                iconPdf = document.createElement('span'),
                txtNroRemito = document.createTextNode(remitos[i]['nroRemito']),
                txtFecha = document.createTextNode(remitos[i]['fecha']);
                
                linkPdf.href = remitos[i]['urlPdf'];
                linkPdf.target = '_blank';
                iconPdf.className = 'glyphicon glyphicon-floppy-disk';
                linkPdf.style = 'color: #F11;';


                nroRemito.appendChild(txtNroRemito);
                fecha.appendChild(txtFecha);
                linkPdf.appendChild(iconPdf);
                pdf.appendChild(linkPdf);

                tr.appendChild(nroRemito);
                tr.appendChild(fecha);
                tr.appendChild(pdf)

                rows.appendChild(tr);
            }

            $tableRemitos.append(rows);
        } else{
            this.$modalRemitos.find('.mensaje-sin-remitos').removeClass('hidden');
            this.$tableRemitos.parent().addClass('hidden');

        }

        this.$modalRemitos.modal('show');
    }

    return { 'init': init };

}   