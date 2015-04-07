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
             var html=new Array(); 
             var counter=4+i+(offset*3);
             html.push('<div id="div'+counter+'" class="panel panel-info panel-body" data-href="'+this.link+'">'); 
             html.push('<div style="margin-bottom:10px;">');
             html.push('<h4 style="padding:0"><a style="color:#1f6692">'+this.title+'</a></h4>');
             html.push('<small style="color:#A36D6D;">发布时间：'+this.pubdate+'<span>');
             html.push('<a href="'+this.link+'" style="float:right;color:#A36D6D" target="_blank"><i class="glyphicon glyphicon-eye-open"></i>查看原文</a></span></small>');
             html.push('</div>');
             html.push(' <div>'+this.descr+this.content+'</div>');
             html.push('</div>');
             $("#scrollText").append($(html).join('')); 
          })
          }
      });
      offset+=1;
      }
    } 
 var length=51;
  for( var i=1;i<length;i++)
  {
    $('#div'+i).click(function(){
      var url=$(this).data('href');
      window.location.href=url;
    });
  } 
}); 
