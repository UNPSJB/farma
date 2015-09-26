$(function() {
    // Create share button
    // new Share('#shareButton');

    $('[data-toggle="tooltip"]').tooltip();

    $('#toggleButton').on('click', function() {
        $(this).find('i').toggleClass('fa-navicon fa-close');
        $('body').toggleClass('doc-nav-shown');
    });

    $('form').each(function() {
        $(this).on('success.form.fv', function(e) {
            e.preventDefault();
        });
    });

    // Create table of contents
    if ($('#toc').length) {
        $('#toc')
            .css('max-width', $('#toc').width())
            .toc({
                selector: '#main h2, #main h3, #main h4',
                elementClass: 'toc',
                ulClass: 'nav',
                indexingFormats: '______'
            });
    }

    // Switch framework handler
    $('iframe.doc-demo-frame').each(function() {
        var $this = $(this);
        $('<div/>').addClass('doc-demo-loader').html('<i class="fa fa-refresh fa-spin fa-2x"></i>').hide().insertBefore($this);
        $this.on('load', function() {
            $(this).prev().hide().end().show();
        });
    });

    $('a[data-demo-framework]').on('click', function(e) {
        e.preventDefault();
        var $this     = $(this),
            framework = $this.attr('data-demo-framework'),
            url       = $this.attr('href'),
            $target   = $($this.attr('data-demo-target'));

        $this
            .closest('.doc-demo')
            .find('.doc-demo-direct a')
            .attr('href', url);

        $this
            .closest('ul')
                .find('li')
                    .removeClass('active')
                    .end()
            .end()
            .parent().addClass('active');

        $this.closest('.dropdown').find('span').eq(0).html($this.html());

        $target
            .closest('.tab-content')
            .find('[data-demo-code]')
                .hide()
                .filter('[data-demo-code="' + framework.toLowerCase() + '"]').show();

        $target.height('');
        $target.hide().prev().fadeIn('fast').promise().then(function() {
            $target.css('visibility', 'hidden').attr('src', url);
        });
    });

    $('.doc-demo').each(function() {
        $(this).find('a[data-demo-framework]').eq(0).click();
    });
    // $('a[data-demo-framework="bootstrap"]').click();
});