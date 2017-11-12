$("input").addClass("form-control");
$("select").addClass("form-control");
$("textarea").addClass("form-control");
$("[id*='time']").timepicki({
		show_meridian:false,
		min_hour_value:0,
		max_hour_value:23,
		step_size_minutes:15,
		overflow_minutes:true,
		increase_direction:'up',
		disable_keyboard_mobile: true
});
$("#id_end_date").dateTimePicker();
$("#id_start_date").dateTimePicker();
$(":checkbox").css({"float": "left", "clear": "both", "margin-top": "-25px",});