$("input").addClass("form-control");
$("select").addClass("form-control");
$("textarea").addClass("form-control");
$('#id_time_of_journey').timepicki({
		show_meridian:false,
		min_hour_value:0,
		max_hour_value:23,
		step_size_minutes:15,
		overflow_minutes:true,
		increase_direction:'up',
		disable_keyboard_mobile: true
});
$('#id_start_time').timepicki({
		show_meridian:false,
		min_hour_value:0,
		max_hour_value:23,
		step_size_minutes:15,
		overflow_minutes:true,
		increase_direction:'up',
		disable_keyboard_mobile: true
});
$('#id_end_time').timepicki({
		show_meridian:false,
		min_hour_value:0,
		max_hour_value:23,
		step_size_minutes:15,
		overflow_minutes:true,
		increase_direction:'up',
		disable_keyboard_mobile: true
});
$('#id_date_of_journey').dateTimePicker();
$('#id_license_validity').dateTimePicker();
$("#id_is_return_journey").css({"float": "left", "clear": "both", "margin-top": "-25px",});