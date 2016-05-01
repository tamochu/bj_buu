$(function() {
	$('#make_calc_list').addInputArea();
	
	$('#make_calc_list').on('change', '.changable', function(){
		list2calc();
	});
	
	function list2calc() {
		var list = new Array();
		$('#make_calc_list li').each(function() {
			list.push({
				group:$(this).find('.group').val(),
				type:$(this).find('.type').val(),
				value:$(this).find('.value').val()
			});
		});
		var max_group = 0;
		for (var i = 0; i < list.length; i++) {
			if (isNaN(list[i].group)) {
				list[i].group = '';
			}
			if (list[i].group !== '' && max_group < list[i].group) {
				max_group = list[i].group;
			}
			
			if (!list[i].type) {
				list[i].type = 'rank';
			}

			if (list[i].value === '') {
				list[i].value = 1;
			}
		}
		for (var i = 0; i < list.length; i++) {
			if (list[i].group !== '') {
				max_group++;
				list[i].group == max_group;
			}
		}
		list.sort(function(a, b){
			return a.group - b.group;
		});
		var calc = list[0].type + ':' + list[0].value + ':1';
		var prev_group = list[0].group;
		for (var i = 1; i < list.length; i++) {
			var glue = '::';
			if (list[i].group != prev_group) {
				glue = ':::';
				prev_group = list[i].group;
			}
			calc += glue + list[i].type + ':' + list[i].value + ':1';
		}
		
		$('#calc').val(calc);
	}
});