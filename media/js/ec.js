function host_option_bind(){
  $(".host_option").bind('click', function(){
    $("#select_host").text($(this).text());
    $("#select_host").data('ishost', $(this).data('ishost'))
  })
}

function project_option_bind(){
  $(".project_option").bind('click', function(){
    $("#select_project").text($(this).text());
    $("#select_project").data('isproject', $(this).data('isproject'))
  })
}

function listbox_check(){
  if($("#select_host").data('ishost')==false){
    alert('Please choose ec host');
    return false;
  }
  if($("#select_project").data('isproject')==false){
    alert('Please choose data project');
    return false;
  }
  return true;
}
