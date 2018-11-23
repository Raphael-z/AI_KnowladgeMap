(function ($) {
    //1.得到$.ajax的对象
    var _ajax = $.ajax;
    $.ajax = function (options) {
        //2.每次调用发送ajax请求的时候定义默认的error处理方法
        var fn = {
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                toastr.error(XMLHttpRequest.responseText, '错误消息', { closeButton: true, timeOut: 0, positionClass: 'toast-top-full-width' });
            },
            success: function (data, textStatus) { },
            beforeSend: function (XHR) { },
            complete: function (XHR, TS) { }
        }
        //3.如果在调用的时候写了error的处理方法，就不用默认的
        if (options.error) {
            fn.error = options.error;
        }
        if (options.success) {
            fn.success = options.success;
        }
        if (options.beforeSend) {
            fn.beforeSend = options.beforeSend;
        }
        if (options.complete) {
            fn.complete = options.complete;
        }
        //4.扩展原生的$.ajax方法，返回最新的参数
        var _options = $.extend(options, {
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                fn.error(XMLHttpRequest, textStatus, errorThrown);
            },
            success: function (data, textStatus) {
                fn.success(data, textStatus);
            },
            beforeSend: function (XHR) {
                fn.beforeSend(XHR);
            },
            complete: function (XHR, TS) {
                fn.complete(XHR, TS);
            }
        });
        //5.将最新的参数传回ajax对象
        _ajax(_options);
    };
})(jQuery);