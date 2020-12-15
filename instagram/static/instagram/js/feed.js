function overlay(insert_button){
    const common_overlay = `<div class="common_overlay" role="presentation">
                            <div class="window" id="window" style="z-index:2;"></div>
                            <div class="common_overlay_div" role="dialog">
                                <div class="common_overlay_div2">
                                    <div class="common_overlay_items" >
                                        ${insert_button}
                                        <button id="cancel_overlay" class="cancel overlay_button" tabindex="0">Cancel</button>
                                    </div>
                                </div>
                            </div>
                        </div>`;
    return common_overlay;
}

function canceloverlay(){
    $('#cancel_overlay').on('click',function(){
        $('.common_overlay').remove();
    });
}


$(function(){
    pageactive('home');
    dropmenu('home');
    dropmenuhide('home');

    $('button.post_option_button').on('click',function(){
        const slug = $(this).data('slug');
        const gotopost = `<button class="gotopost overlay_button" tabindex="0">Go to post</button>`;
        const olay = overlay(gotopost);
        $('body').append(olay);
        $('.gotopost').click(function(){
            const cl = window.location;
            window.location=`${cl}post/${slug}`;
        });
        canceloverlay();
    });

    $(".icon-love").on("click",function(e){
        p_id = $(this).data('id');

        const unlike = `<span class="love-span2">
                        <svg aria-label="Unlike" id="love${p_id}" class="icon" fill="#ed4956" height="24" viewBox="0 0 48 48" width="24">
                            <path d="M34.6 3.1c-4.5 0-7.9 1.8-10.6 5.6-2.7-3.7-6.1-5.5-10.6-5.5C6 3.1 0 9.6 0 17.6c0 7.3 5.4 12 
                            10.6 16.5.6.5 1.3 1.1 1.9 1.7l2.3 2c4.4 3.9 6.6 5.9 7.6 6.5.5.3 1.1.5 1.6.5s1.1-.2 1.6-.5c1-.6 2.8-2.2 
                            7.8-6.8l2-1.8c.7-.6 1.3-1.2 2-1.7C42.7 29.6 48 25 48 17.6c0-8-6-14.5-13.4-14.5z"></path>
                        </svg>
                    </span>`;
        const like   = `<span class="love-span2">
                            <svg class="icon" id="love${p_id}" aria-label="Like" fill="#262626" height="24" viewBox="0 0 48 48" width="24">
                                <path d="M34.6 6.1c5.7 0 10.4  5.2 10.4 11.5 0 6.8-5.9 11-11.5 16S25 41.3 24 
                                41.9c-1.1-.7-4.7-4-9.5-8.3-5.7-5-11.5-9.2-11.5-16C3 11.3 7.7 6.1 13.4 6.1c4.2 0 6.5 2 8.1 4.3 
                                1.9 2.6 2.2 3.9 2.5 3.9.3 0 .6-1.3 2.5-3.9 1.6-2.3 3.9-4.3 8.1-4.3m0-3c-4.5 0-7.9 1.8-10.6 
                                5.6-2.7-3.7-6.1-5.5-10.6-5.5C6 3.1 0 9.6 0 17.6c0 7.3 5.4 12 10.6 16.5.6.5 1.3 1.1 1.9 1.7l2.3 
                                2c4.4 3.9 6.6 5.9 7.6 6.5.5.3 1.1.5 1.6.5.6 0 1.1-.2 1.6-.5 1-.6 2.8-2.2 7.8-6.8l2-1.8c.7-.6 
                                1.3-1.2 2-1.7C42.7 29.6 48 25 48 17.6c0-8-6-14.5-13.4-14.5z"></path>
                            </svg>
                        </span>`;

        e.preventDefault();
        $.ajax({
            type: 'get',
            url : editlikelink,
            data: {
                id: p_id,
                event: $(`#love${p_id}`).attr('aria-label')
            },
            success:function(data){
                $(`#love-div-${p_id}`).empty();
                if(data.button==='Like')
                    $(`#love-div-${p_id}`).append(like);
                else
                    $(`#love-div-${p_id}`).append(unlike);
                like_button_response(data);
            },
            error:function(e){
                console.log(e);
            }
        });
    });

    function like_button_response(data){
        if(data.total_likes==0)
            $(`#post_likes_${data.post_id}`).remove();
        else if(data.total_likes==1){
            $(`#post_likes_${data.post_id}`).remove();
            const wholikesit = `<section class="post_likes" id="post_likes_${data.post_id}" >
                                    <div class="post_likes_div">
                                        <div class="first_liker_propic_div">
                                            <div class="first_liker_propic_div2">
                                                <span class="first_liker_propic_span">
                                                    <img class="first_liker_propic" src="${data.last_liker_propic}" alt="${data.last_liker_name}'s propic"/>
                                                </span>
                                            </div>
                                        </div>
                                        <div class="who_likes_it" id="who_likes_it_${data.post_id}">Liked by <span class="first_liker_span"><a class="first_liker_prolink" href="/${data.last_liker_name}/">${data.last_liker_name}</a></span></div>
                                    </div>
                                </section>`
            $(`#pd_post_likecomment_${data.post_id}`).append(wholikesit);
        }else{
            if(data.total_likes>2 || data.button==='Like')
                $(`#total_liker_button_${data.post_id}`).html(`<span>${data.total_likes-1}</span> other${data.total_likes-1 > 1 ? "s" : ""}`);
            else
                $(`#who_likes_it_${data.post_id}`).append(` and <button class="total_liker_button" id="total_liker_button_${data.post_id}"><span>${data.total_likes-1}</span> other</button>`);
        }
    }

    $('textarea').keyup(function (e) {
        const pid = $(this).data('id');
        if(e.shiftKey && e.which==13){
            e.preventDefault()
            $(`#comment_post_button${pid}`).removeAttr('disabled')
        }else if(e.which==8||(this.value.length && e.which!=13)){
            if(this.value.length){
                e.preventDefault()
                $(`#comment_post_button${pid}`).removeAttr('disabled')
            }else{
                $(`#comment_post_button${pid}`).attr('disabled','enabled')
            }
        }else if(this.value.length && e.which==13){
            if($(`#comment_post_button${pid}`).attr('disabled')){
                this.value=""
            }
            else{
                $(`#comment_post_button${pid}`).click();
                this.value="";
            }
        }else
            $(`#comment_post_button${pid}`).attr('disabled','enabled')
    });

    $(".comment_input_form").on("submit",function(e){
        const pid = $(this).data('id');
        e.preventDefault();
        $.ajax({
            type:   "post",
            url:    addcommentlink,
            data:{
                comment : $(`#comment_textarea${pid}`).val(),
                total_comment : $(this).data('t_comment'),
                post_id : pid,
                csrfmiddlewaretoken : $("input[name=csrfmiddlewaretoken]").val()
            },
            success: function(response){
                $(`#comment_input_form${pid}`).trigger("reset");
                $(`#comment_input_form${pid}`).data("t_comment",response.total_comment);
                $(`#comment_post_button${pid}`).attr('disabled','true')
                newcomment(response,pid);
                
            },
            error: function(e){
                console.log(e);
            }
        });
    });

    function newcomment(data,postid){
        id = postid;
        name = data.name;
        comment = data.comment;
        tc = data.total_comment;
        const newcomment = `<div class="common_comment_class first_last_comment_div amb">
                                <div class="main_comment_div">
                                    <span class="commenter_span"><a class="commenter_link" href="/${name}/">${name}</a></span>
                                    <span class="comment_span"><span>${comment}</span></span>
                                </div>
                            </div>`;
        const zeronewcomment = `<div id="main_comment_box${id} >
                                    ${newcomment}
                                </div>`
        if(tc>1)
            $(`#main_comment_box${id}`).append(newcomment);
        else
            $(`#post_comment_box_${id}`).append(zeronewcomment);
    }


});