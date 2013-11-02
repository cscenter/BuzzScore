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
                var link = $(this);
                var url = getUrl(link);
                $.get(url, null, function (html) {
                    link.before(html);
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
