/**
 * Created by nikita_kartashov on 26/10/2013.
 */
(function ($) {
    $.fn.paginate = function () {
        var moreSelector = 'a#more-link';

        var getUrl = function(link) {
            return link.attr('href')
            };

        return this.each(function() {
            $(this).on('click', moreSelector, function(e) {
                displaySpinner();
                var link = $(this);
                var url = getUrl(link);
                $.ajax(url)
                    .success(function(html) {
                        link.before(html);
                    })
                    .error(function() {
                        link.before($("<div>We're really sorry, but somthing seems to have broken</div>"))
                    })
                    .complete(function() {
                        hideSpinner();
                        link.remove();
                    });
                return false;
            });
        });
    };

    $.paginate = function() {
        return $('body').paginate();
    }
} (jQuery));
