// $(function () {
//     $("#myform").submit(function () {
//         //拿用户名判断是否符合条件
//         var uname = $("#uid").val();
//         var confirm_pwd = $("#u_confirm_id").val();
//         var pwd = $("#u_pwd").val();
//
//         if (uname.length <3) {
//             alert("用户名过短");
//             //阻止提交
//             return false;
//         }
//
//     //    判断密码长度
//         if (pwd.length<3) {
//             alert("密码过短");
//             return false;
//         }
//     //    判断密码个确认密码
//         if (pwd != confirm_pwd){
//             alert("两次密码输入不一致");
//             return false;
//         }
//     //    通过以上校验 我们加密密码和确认密码
//         var pwd_md5 = md5(pwd);
//         var c_pwd_md5 = md5(confirm_pwd);
//
//     //    将加密的值设置回去
//         $("#u_pwd").val(pwd_md5);
//         $("#u_confirm_pwd").val(c_pwd_md5);
//     })
//
//  })
$(function () {
    $("#myform").submit(function () {
        //    拿用户名 判断不能为空 并且大于三位
        var name = $("#uid").val();
        if (name.length < 3) {
            alert("用户名过短");
            //阻止提交
            return false;
        }
        var pwd = $("#u_pwd").val();
        var confirm_pwd = $("#u_confirm_pwd").val();
        if (pwd == confirm_pwd & pwd.length >= 6) {
            //    做加密
            var enc_pwd = md5(pwd);
            var enc_confirm_pwd = md5(confirm_pwd);
            //    设置回去
            $("#u_pwd").val(enc_pwd);
            $("#u_confirm_pwd").val(enc_confirm_pwd);
            console.log(enc_pwd);
        } else {
            alert("密码过短或不一致");
            return false;
        }

    });
    $("#uid").change(function () {
        var uname = $("#uid").val();
            $.ajax({
                url:"/app/check_name",
                data:{
                    uname: uname
                },
                method:"get",
                success:function (res) {
                //    提示用户
                    if (res.code == 1){
                        $("#uname_msg").html(res.msg);
                    }else {
                    //    错误提示，别用弹窗减少用户操作
                        alert(res.msg);

                    }

                }

            });

    })
})
