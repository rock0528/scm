$(document).ready(function(){
    document.jsonService = new JsonRpc.ServiceProxy("/json/", {
        asynchronous: true,
        methods: ["ec.get_schedules", "ec.backup_schedules", "ec.restore_schedules"]
    });

    initialize();
    events_handle();
})

function initialize(){
  $("#wait_box").hide();
  $("#backup").attr("disabled", "true");
  $("#restore").attr("disabled", "true");
}

function events_handle(){
  host_option_bind();
  project_option_bind();
  get_bind();
  backup_bind();
  restore_bind();
}

function restore_bind(){
  $("#restore").bind('click', function(){
    if(listbox_check()==false){
      return;
    }
    $("#wait_box").show();
    host_name = $("#select_host").text();
    project_name = $("#select_project").text();
    JsonRpc.setAsynchronous(document.jsonService, true);
    document.jsonService.ec.restore_schedules({
            params: [host_name, project_name],
            onSuccess: function(result) {
              show_result(result)
              $("#wait_box").hide();
            }
        });
  })
}


function backup_bind(){
  $("#backup").bind('click', function(){
    if(listbox_check()==false){
      return;
    }
    $("#wait_box").show();
    host_name = $("#select_host").text();
    project_name = $("#select_project").text();
    JsonRpc.setAsynchronous(document.jsonService, true);
    document.jsonService.ec.backup_schedules({
            params: [host_name, project_name],
            onSuccess: function(result) {
              show_result(result)
              $("#wait_box").hide();
            }
        });
  })
}

function get_bind(){
  $("#get").bind('click', function(){
    if(listbox_check()==false){
      return;
    }
    $("#wait_box").show();
    host_name = $("#select_host").text();
    project_name = $("#select_project").text();
    JsonRpc.setAsynchronous(document.jsonService, true);
    document.jsonService.ec.get_schedules({
            params: [host_name, project_name],
            onSuccess: function(result) {
              show_result(result)
              $("#wait_box").hide();
            }
        });
  })
}

function show_result(result){
  $("#schedule_result").empty();
  if(!result){
    $("#backup_time").text("NA");
    $("#store_info").text("Nothing can be restored.");
    $("#store_info").css('color', 'white');
    $("#restore").attr("disabled", "disabled");
    $("#backup").removeAttr("disabled");
    return;
  }
  backup_time = result["backup_time"];
  $("#backup_time").text(backup_time);
  is_restore = result["is_restore"];
  if(is_restore){
    $("#store_info").text("The last backup has been restored already.");
    $("#store_info").css('color', 'white');
    $("#restore").attr("disabled", "disabled");
    $("#backup").removeAttr("disabled");
  }else{
    $("#store_info").text("The last backup hasn't been restored yet, please remember to restore it.");
    $("#store_info").css('color', 'red');
    $("#restore").removeAttr("disabled");
    $("#backup").attr("disabled", "disabled");
  }

  data = result["schedules"];
  schedule_result_table_html = schedule_result_table_header();
  schedule_result_table_html += schedule_result_table_body(data);
  $("#schedule_result").html(schedule_result_table_html);
  $('#schedule_result_table').fixedHeaderTable({
  	footer: false,
  	cloneHeadToFoot: false,
  	altClass: 'odd',
  	autoShow: true
  });
}

function schedule_result_table_body(result){
  tableHtml = '<tbody>';
  for(name in result){
    enable = result[name];
    tableHtml +='<tr><td style="width:40%">'+name+'</td>';
    tableHtml +='<td style="width:20%">'+enable+'</td></tr>';
  }
  tableHtml += '</tbody></table>';
  return tableHtml;
}

function schedule_result_table_header(){
  tableHtml = '<table id="schedule_result_table" class="fancyDarkTable">';
	tableHtml += '<thead><tr>'+
    						'<th style="">Schedule Name</th>'+
    						'<th style="">Enable State</th>';
	tableHtml += '</tr></thead>';
  return tableHtml;
}
