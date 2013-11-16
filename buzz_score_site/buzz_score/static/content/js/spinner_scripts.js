/**
 * Created by nikita_kartashov on 16/11/2013.
 */
function displaySpinner() {

    function createCenterDiv() {
        $('<div/>')
            .attr('id', 'centerSpinnerDiv')
            .attr('style', 'position:fixed;top:50%;left:50%').appendTo('#wrap')
    }

    var opts = {
                lines: 11, // The number of lines to draw
                length: 10, // The length of each line
                width: 5, // The line thickness
                radius: 12, // The radius of the inner circle
                corners: 1, // Corner roundness (0..1)
                rotate: 0, // The rotation offset
                direction: 1, // 1: clockwise, -1: counterclockwise
                color: '#000', // #rgb or #rrggbb or array of colors
                speed: 0.5, // Rounds per second
                trail: 50, // Afterglow percentage
                shadow: false, // Whether to render a shadow
                hwaccel: false, // Whether to use hardware acceleration
                className: 'spinner', // The CSS class to assign to the spinner
                zIndex: 2e9, // The z-index (defaults to 2000000000)
                top: 'auto', // Top position relative to parent in px
                left: 'auto' // Left position relative to parent in px
            };
            createCenterDiv();
            $('#centerSpinnerDiv').spin(opts);
        }

function hideSpinner() {
    $('#centerSpinnerDiv').spin(false);
}
