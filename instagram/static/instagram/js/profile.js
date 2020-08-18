const change_profile_pic_form = `${csrf}
                                <input type="file" name="propic" style="display: none !important;">`;

const change_profile_pic_overlay = `<div class="change_propic_overlay" role="presentation">
                                        <div class="change_propic" role="dialog">
                                            <div class="change_propic_item">
                                                <div class="change_propic_header">
                                                    <h3 class="cng_pic">Change Profile Photo</h3>
                                                </div>
                                                <div style="margin-top:16px;">
                                                    <button id="cng" class="cng cng_pic_button" tabindex="0">Upload Photo</button>
                                                    <button id="rmv" class="rmv cng_pic_button" tabindex="0">Remove Current Photo</button>
                                                    <button class="cancel cng_pic_button" tabindex="0">Cancel</button>
                                                    ${change_profile_pic_form}
                                                </div>
                                            </div>
                                        </div>
                                    </div>`;

function change_pic_form(action){
    if (action ==='add'){
        $('.propic-div').children('div').append(change_profile_pic_form);
    }else{
        $('.propic-div').children('div').empty();
    }
}

$(function () {

    change_pic_form('add');

    function on_success(url,action){
        if(action!=='default_change'){
            $('.change_propic_overlay').remove();
            change_pic_form('add');
            if (action==='change'){
                $('img.propic').attr({
                    src:url,
                    alt:'change pro pic'
                })
                $('button.propic-button').attr('title','change')
            }else{
                $('img.propic').attr({
                    src:url,
                    alt:'add pro pic'
                })
                $('button.propic-button').attr('title','add')
            }
        }else{
            $('img.propic').attr({
                src:url,
                alt:'change pro pic'
            })
            $('button.propic-button').attr('title','change')
        }
    }

    function send_ajax_request(method,DATA,bool){
        $.ajax({
            type:method,
            url:URL,
            processData: bool,
            contentType: bool,
            data: DATA,
            success: function(response){
                on_success(response.url,response.action)
            },
            error:function(e){
                console.log(e)
            }
        });     
    }
    

    $('div.propic-div').on('click','button',function () {
        if ($(this).attr('title')==='change'){
            change_pic_form('empty');
            $('body').append(change_profile_pic_overlay);
        }else{
            $("input[name='propic']").click().on('change',function(){
                var fd = new FormData()
                fd.append('imgfile',$("input[name='propic']")[0].files[0])
                fd.append('csrfmiddlewaretoken',$("input[name='csrfmiddlewaretoken']").val())
                fd.append('action','default_change')
                send_ajax_request('post',fd,false)
            })
        }
        
    });


    $('body').on('click','.change_propic_overlay',function (e) {
        var clicked = $(e.target);
        if (clicked.is('.cancel')||(!clicked.is('.change_propic') && !clicked.parents().is('.change_propic'))) {
            $('body').attr('style', 'overflow:scroll;');
            $('.change_propic_overlay').remove();
            change_pic_form('add');
        }else{
            if (clicked.is('.cng')){
                $("input[name='propic']").click().on('change',function(){
                    var fd = new FormData()
                    fd.append('imgfile',$("input[name='propic']")[0].files[0])
                    fd.append('csrfmiddlewaretoken',$("input[name='csrfmiddlewaretoken']").val())
                    fd.append('action','change')
                    send_ajax_request('post',fd,false)
                })
            }else if (clicked.is('.rmv')){
                data = {action : 'remove'}
                send_ajax_request('get',data,true)
            }
        }
    });
});