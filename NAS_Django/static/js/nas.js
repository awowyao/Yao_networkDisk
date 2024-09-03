function GetDir() {
    $(".Dir").bind("click", function() {
        var show = "";
        var conten = $(".DirFillName",this).text()
        console.log(conten)
        alert(conten);
        // $.post("../char", {'conten':conten},function (data) {
            // $.each(data["data"], function (i,obj) {
            //     show += '<li class=\"comm_each line_top margin\">';
            //     show += "<img class='comm_avat part_roun' src='https://img2.doubanio.com/view/photo/l/public/p1476914173.webp'/>"
            //     show += '<div class="comm_head">';
            //     show += '<strong class="text_line">'+ obj.user+ '</strong>';
            //     show += '<span class="part_tips hidden_mb"><span class="split_line"></span><span class="mycol">248#</span></span>';
            //     show += '<span class="part_tips hidden_xs">' + obj.time + '<span class="split_line"></span>';
            //     show += '</div>';
            //     show += '<div class="comm_cont">';
            //     show += '<div class="comm_content">'+ obj.content +'</div></div>';
            //     show += '</li>';
            // })
            // $(".pull_right #lennub").text(data["data_len"])
            // $(".part_rows").html(show)
        // }, 'json')

    })
}

function Getfill() {
    $(".Fill").bind("click", function() {
        var show = "";
        var conten = $(".DirFillName",this).text()
        console.log(conten)
        alert(conten);
        // $.post("../char", {'conten':conten},function (data) {
            // $.each(data["data"], function (i,obj) {
            //     show += '<li class=\"comm_each line_top margin\">';
            //     show += "<img class='comm_avat part_roun' src='https://img2.doubanio.com/view/photo/l/public/p1476914173.webp'/>"
            //     show += '<div class="comm_head">';
            //     show += '<strong class="text_line">'+ obj.user+ '</strong>';
            //     show += '<span class="part_tips hidden_mb"><span class="split_line"></span><span class="mycol">248#</span></span>';
            //     show += '<span class="part_tips hidden_xs">' + obj.time + '<span class="split_line"></span>';
            //     show += '</div>';
            //     show += '<div class="comm_cont">';
            //     show += '<div class="comm_content">'+ obj.content +'</div></div>';
            //     show += '</li>';
            // })
            // $(".pull_right #lennub").text(data["data_len"])
            // $(".part_rows").html(show)
        // }, 'json')

    })
}

$(function () {
    GetDir();
    // Getfill();
});
