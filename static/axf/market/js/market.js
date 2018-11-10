var type_dowm = true;
var sort_dowm = true;

$(function () {
    //给点击类型加点击事件
    $("#all_cate").click(all_type_event);
    $("#cates").click(all_type_event);
    //排序
    $("#all_sort").click(all_sort_event);
    $("#sorts").click(all_sort_event);
//    加操作
    $(".addShopping").click(function () {
        $current_bt = $(this);
        //    获取点击的商品id
        var g_id = $current_bt.attr("g_id");


        //发送请求给后端
        $.ajax({
            url: "/app/cart_api",
            data: {
                g_id: g_id,
                type: "add"
            },

            method: "post",
            success: function (res) {
                console.log(res);
                if (res.code == 1) {
                    $current_bt.prev().html(res.data);
                }
                if (res.code == 2) {
                    //    跳转到登录
                    window.open(res.data, target = "_self");
                }

            }
        });

    })

    $(".subShopping").click(function () {
        $current_bt = $(this);
        //    获取点击的商品id
        var g_id = $current_bt.attr("g_id");
        //判断是不是0,0就不返回，返回return
        if ($current_bt.next().html() == "0") {
            return;
        }
        $.ajax({
            url: "/app/cart_api",
            data: {
                g_id: g_id,
                type: "sub"
            },

            method: "post",
            success: function (res) {
                console.log(res);
                if (res.code == 1) {
                    $current_bt.next().html(res.data);
                }
                if (res.code == 2) {
                    //    跳转到登录
                    window.open(res.data, target = "_self");
                }

            }
        });
    });
})
function all_type_event() {
    $("#cates").toggle()
    var type_span = $("#all_cate").find("span");
    if (type_dowm == true) {
        //如果是向下的状态 那改变原有的类样式 修改状态值
        type_span.removeClass("glyphicon glyphicon-chevron-down").addClass("glyphicon glyphicon-chevron-up");
        type_dowm = false;
    } else {
        type_span.removeClass("glyphicon glyphicon-chevron-up").addClass("glyphicon glyphicon-chevron-down");
        type_dowm = true;
    }
}

function all_sort_event() {
    $("#sorts").toggle()
    var type_span = $("#all_sort").find("span");
    if (sort_dowm == true) {
        //如果是向下的状态 那改变原有的类样式 修改状态值
        type_span.removeClass("glyphicon glyphicon-chevron-down").addClass("glyphicon glyphicon-chevron-up");
        sort_dowm = false;
    } else {
        type_span.removeClass("glyphicon glyphicon-chevron-up").addClass("glyphicon glyphicon-chevron-down");
        sort_dowm = true;
    }
}