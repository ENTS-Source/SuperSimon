$(window).load(function () {
    $('.loading-container').fadeOut(1000, function () {
        $(this).remove();
    });
});

$(function () {
    $(document).on('click', '.navbar-toggle', function () {
        $('aside.left-panel').toggleClass('collapsed');
    });
    $("aside.left-panel nav.navigation > ul > li:has(ul) > a").click(function () {
        if ($("aside.left-panel").hasClass('collapsed') == false || $(window).width() < 768) {
            $("aside.left-panel nav.navigation > ul > li > ul").slideUp(300);
            $("aside.left-panel nav.navigation > ul > li").removeClass('active');
            if (!$(this).next().is(":visible")) {
                $(this).next().slideToggle(300, function () { $("aside.left-panel:not(.collapsed)").getNiceScroll().resize(); });
                $(this).closest('li').addClass('active');
            }
            return false;
        }
    });
    if ($.isFunction($.fn.popover)) {
        $('.popover-btn').popover();
    }
    if ($.isFunction($.fn.tooltip)) {
        $('.tooltip-btn').tooltip()
    }
    if ($.isFunction($.fn.niceScroll)) {
        $(".nicescroll").niceScroll({
            cursorcolor: '#9d9ea5',
            cursorborderradius: '0px'
        });
    }
    if ($.isFunction($.fn.niceScroll)) {
        $("aside.left-panel:not(.collapsed)").niceScroll({
            cursorcolor: '#8e909a',
            cursorborder: '0px solid #fff',
            cursoropacitymax: '0.5',
            cursorborderradius: '0px'
        });
    }
    if ($.isFunction($.fn.inputmask)) {
        $(".inputmask").inputmask();
    }
    if ($.isFunction($.fn.tagsinput)) {
        $('.tagsinput').tagsinput();
    }
    if ($.isFunction($.fn.chosen)) {
        $('.chosen-select').chosen();
        $('.chosen-select-deselect').chosen({ allow_single_deselect: true });
    }
    if ($.isFunction($.fn.datetimepicker)) {
        $('#datetimepicker').datetimepicker();
        $('#datepicker').datetimepicker({ pickTime: false });
        $('#timepicker').datetimepicker({ pickDate: false });

        $('#datetimerangepicker1').datetimepicker();
        $('#datetimerangepicker2').datetimepicker();
        $("#datetimerangepicker1").on("dp.change", function (e) {
            $('#datetimerangepicker2').data("DateTimePicker").setMinDate(e.date);
        });
        $("#datetimerangepicker2").on("dp.change", function (e) {
            $('#datetimerangepicker1').data("DateTimePicker").setMaxDate(e.date);
        });
    }
    if ($.isFunction($.fn.wysihtml5)) {
        $('.wysihtml').wysihtml5();
    }
    if ($.isFunction($.fn.ckeditor)) {
        CKEDITOR.disableAutoInline = true;
        $('#ckeditor').ckeditor();
        $('.inlineckeditor').ckeditor();
    }
    $('.scrollToTop').click(function () {
        $('html, body').animate({ scrollTop: 0 }, 800);
        return false;
    });
});

function toggleFullScreen() {
    if ((document.fullScreenElement && document.fullScreenElement !== null) || (!document.mozFullScreen && !document.webkitIsFullScreen)) {
        if (document.documentElement.requestFullScreen) {
            document.documentElement.requestFullScreen();
        } else if (document.documentElement.mozRequestFullScreen) {
            document.documentElement.mozRequestFullScreen();
        } else if (document.documentElement.webkitRequestFullScreen) {
            document.documentElement.webkitRequestFullScreen(Element.ALLOW_KEYBOARD_INPUT);
        }
    } else {
        if (document.cancelFullScreen) {
            document.cancelFullScreen();
        } else if (document.mozCancelFullScreen) {
            document.mozCancelFullScreen();
        } else if (document.webkitCancelFullScreen) {
            document.webkitCancelFullScreen();
        }
    }
}
