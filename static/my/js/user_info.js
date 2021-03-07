var $nickname_input = $("#nickname");
var $userid_input = $("#userid");
var $age_input = $("#age");
var $sex_input = $("input[name='sex']");
var $birthday_input = $("#birthday");
var $hometown_input = $("#hometown");
var $introduce_input = $("#introduce");
$(".edit").on("click", function(){
    var innerText = $(this).html();
    if (innerText.search("完成") === -1){
        $nickname_input.removeAttr("disabled");
        $userid_input.parent().next().find("span").html("用户ID不可变");
        $age_input.removeAttr("disabled");
        $sex_input.removeAttr("disabled");
        $birthday_input.removeAttr("disabled");
        $hometown_input.removeAttr("disabled");
        $introduce_input.removeAttr("disabled");
        $(this).html("<span><span class='glyphicon glyphicon-ok'></span>&nbsp;完成</span>")
    } else {
        var nickname_txt = $nickname_input.val();
        if (nickname_txt.length === 0){
            $nickname_input.parent().next().find("span").html("用户昵称不能为空");
            return;
        }
        update_info(nickname_txt, $age_input.val(), $("input[name='sex']:checked").val(), $birthday_input.val(),
            $hometown_input.val(), $introduce_input.val());
        $nickname_input.attr("disabled","disabled");
        $userid_input.attr("disabled","disabled");
        $userid_input.parent().next().find("span").html("");
        $age_input.attr("disabled","disabled");
        $sex_input.attr("disabled","disabled");
        $birthday_input.attr("disabled","disabled");
        $hometown_input.attr("disabled","disabled");
        $introduce_input.attr("disabled","disabled");
        $(this).html("<span><span class=\"glyphicon glyphicon-pencil\"></span>&nbsp;编辑</span>")
    }
});

$('#avatar').on('change', function (event) {
    var file = this.files[0];
    var formData = new FormData();
    console.log(file);
    formData.append("avatar", file);
    $.ajax({
        url: "/user/update_avatar/",
        method: "post",
        processData: false,
        contentType: false,
        dataType: "json",
        data: formData,
        success: function (data) {
            console.log(data);
            if (data.status === 0){
                $('.user-avatar').attr({"src": data.data})
                $('.nav-avatar').attr({"src": data.data})
            }else {
                alert(data.msg);
            }
        }
    })
});

function update_info(nickname, age, sex, birthday, hometown, userInfo) {
    if (nickname.length === 0){
        return;
    }
    $.ajax({
        url: "/user/update_user_info/",
        method: "post",
        dataType: "json",
        data: {nickname: nickname, age: age, sex: sex, birthday: birthday, hometown: hometown, userInfo: userInfo},
        success: function (data) {
            console.log("更新用户返回数据：");
            console.log(data);
            if (data.status === 0){
                //
                $userid_input.val(data.data.username);
                $nickname_input.val(data.data.user_nick);
                $(".user-nick").html("用户昵称：" + data.data.user_nick);
                $(".nav-greet").html("欢迎回来：" + data.data.user_nick + "&nbsp;(用户ID：" + data.data.username + ")");
                $age_input.val(data.data.age);
                $birthday_input.val(data.data.birthday);
                $hometown_input.val(data.data.hometown);
                $introduce_input.val(data.data.user_info);

                var sex_ele_id = "";
                if (data.data.sex === 1){
                    sex_ele_id = "man";
                } else if (data.data.sex === 0){
                    sex_ele_id = "woman";
                } else {
                    return;
                }
                $sex_input.each(function(){$(this).removeAttr("checked")});
                $("#"+sex_ele_id).attr("checked","checked");
            } else if (data.status === 1) {
                console.log(data.msg)
            }
        }
    })
}