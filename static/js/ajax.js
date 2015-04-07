      var offset=0;
      $(window).scroll(function(){
        if(parseFloat($(window).scrollTop())+parseFloat($(window).height())>=$(document).height()-400) 
        { 
          var url=window.location.href;
          url =url+'?offset='+offset;
          if(offset<10){
             $.getJSON(url, function(item){
              if(item!=""){
                $(item).each(function(i){
                 var html=""; 
                 var counter=11+i+(offset*5);
                 html+='<div id="div'+counter+'"class="panel panel-info panel-body" data-href="/article/'+this.id+'/">';
                 html+='<div style="margin-bottom:10px;">';
                 html+='<h4 style="color:#428bca;padding:0"><a href="/article/'+this.id+'/">'+this.title+'</a></h4>';
                 html+='<small style="color:#A36D6D;">发布时间：'+this.pubdate+'</small>';
                 html+='</div>';
                 html+='<div class="brief-img">'+this.brief+'</div>';
                 html+='<a style="float:right;clear:both" href="/article/'+this.id+'/">阅读<i class="glyphicon glyphicon-eye-open"></i></a>';
                 html+='</div>';
                $("#scrollText").append($(html));     
              })
              }
          });
          offset+=1;
          }
        } 
        todetail;
         
      });

      todetail();

function todetail(){
  var length=51;
          for( var i=1;i<length;i++)
          {
            $('#div'+i).click(function(){
              var url=$(this).data('href');
              window.location.href=url;
            });
          }
}