$(document).ready(function () {
    $("#gz_ph_xz").mouseenter(function () {
        $("#gz_phb").show();
        $("#dz_phb").hide();
        $("#gz_ph_xz").css({"background-color": "#337ab7", "color": "#fff", "border-color": "#337ab7"})
        $("#dz_ph_xz").css({"background-color": "#fff", "color": "#000", "border-color": "#ddd"})
    });

    $("#dz_ph_xz").mouseenter(function () {
        $("#gz_phb").hide();
        $("#dz_phb").show();
        $("#gz_ph_xz").css({"background-color": "#fff", "color": "#000", "border-color": "#ddd"})
        $("#dz_ph_xz").css({"background-color": "#337ab7", "color": "#fff", "border-color": "#337ab7"})
    });

    $.ajax(
        {
            url: '/user/phb_list/',
            // type: 'post',
            dataType: 'json',
            async: 'false',
            // data:{
            //     "userName":userName,
            //     "passWord":passWord,
            // },
            success: function (data) {
                if (data.status == 200) {
                    console.log(data)
                } else {
                    console.log("请求数剧失败");
                }
            },
            error: function (data) {
                console.log("请求数剧失败");
            },
        }
    );
});
