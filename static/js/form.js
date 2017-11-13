$("input").addClass("form-control");
$("select").addClass("form-control");
$("textarea").addClass("form-control");
if($("[id*='time']").length) {
    $("[id*='time']").timepicki({
        show_meridian: false,
        min_hour_value: 0,
        max_hour_value: 23,
        step_size_minutes: 15,
        overflow_minutes: true,
        increase_direction: 'up',
        disable_keyboard_mobile: true
    });
}
if($("#id_end_date").length) {
	$("#id_end_date").dateTimePicker();
}
if($("#id_start_date").length) {
	$("#id_start_date").dateTimePicker();
}
if($("#id_license_validity").length) {
	$("#id_license_validity").dateTimePicker();
}
if($("#id_phone").length) {
    $("#id_phone").attr('placeholder', "eg: +91-XXXXXXXXXX");
}
if($("#id_emergency_contact").length) {
    $("#id_emergency_contact").attr('placeholder', "eg: +91-XXXXXXXXXX");
}
if($("#id_registration_no").length) {
    $("#id_registration_no").attr('placeholder', "eg: UP 15 D 1234");
}
if($("#id_nickname").length) {
    $("#id_nickname").attr('placeholder', "eg: B3");
}
$(":checkbox").css({"float": "left", "clear": "both", "margin-top": "-25px",});