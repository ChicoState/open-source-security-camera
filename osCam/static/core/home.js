

function main(){

    window.onresize = function(ev) { 
        var expandCollapse = function(){
            if ( $(window).width() < 768 ) {
                $(function(){
                    // add a class .collapse to a div .showHide
                    $('.div-info').addClass('collapse');
                    // set display: "" in css for the toggle button .btn.btn-primary
                    $('.div-info').css('display', ' ');// removes display property to make it visible
                });
            }
            else {
                $(function(){
                    // remove a class .collapse from a div .showHide
                    $('.div-info').removeClass('collapse');
                    // set display: none in css for the toggle button .btn.btn-primary  
                    $('.div-info').css('display', 'none');// hides button display on bigger screen
                });
            }
        }
        $(window).resize(expandCollapse); 
    };

}

window.onload=main;
