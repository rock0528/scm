$(document).ready(function(){
    document.jsonService = new JsonRpc.ServiceProxy("/json/", {
        asynchronous: true,
        methods: ["ec.search_property"]
    });

    initialize();
    events_handle();
})

function initialize(){
  $("#wait_box").hide();
}

function events_handle(){
  host_option_bind();
  project_option_bind();
  search_text_bind();
  search_bind();
}

function search_text_bind(){
  $("#search_text").bind('click', function(){
    if($("#search_text").val()=='search property'){
      $("#search_text").val('');
    }
  })
}

function search_bind(){
  $("#search").bind('click', function(){
    if(listbox_check()==false){
      return;
    }
    if(!$("#search_text").val() || $("#search_text").val()=='search property'){
      alert('Please input search property');
      return;
    }
    $("#search_result").empty();
    $("#wait_box").show();
    data_interact();
  })
}

function data_interact(){
  host_name = $("#select_host").text();
  project_name = $("#select_project").text();
  search_property = $("#search_text").val().trim();
  JsonRpc.setAsynchronous(document.jsonService, true);
  document.jsonService.ec.search_property({
          params: [host_name, project_name, search_property],
          onSuccess: function(result_list) {
            property_result_table_html = property_result_table_header();
            property_result_table_html += property_result_table_body(result_list);
            $("#search_result").html(property_result_table_html);
          	$('#property_result_table').fixedHeaderTable({
          		footer: false,
          		cloneHeadToFoot: false,
          		altClass: 'odd',
          		autoShow: true
          	});
            $("#wait_box").hide();
          }
      });
}

function property_result_table_body(result_list){
  tableHtml = '<tbody>';
  for(i in result_list){
    path = result_list[i].split('|')[0];
    value = result_list[i].split('|')[1];
    tableHtml +='<tr><td style="width:50%">'+path.replace(/\//g, ' / ')+'</td>';
    tableHtml +='<td style="width:20%"><input type="text" style="width:80%" value="'+value+'"</input></td></tr>';
  }
  tableHtml += '</tbody></table>';
  return tableHtml;
}

function property_result_table_header(){
  tableHtml = '<table id="property_result_table" class="fancyTable">';
	tableHtml += '<thead><tr>'+
    						'<th style="">Path</th>'+
    						'<th style="">Value</th>';
	tableHtml += '</tr></thead>';
  return tableHtml;
}
