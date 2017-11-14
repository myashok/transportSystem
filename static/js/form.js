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
    $("#id_phone").after("<p>eg: +91-XXXXXXXXXX</p>");
    $("#id_phone").next().css("font-size", "85%");
}
if($("#id_emergency_contact").length) {
    $("#id_emergency_contact").after("<p>eg: +91-XXXXXXXXXX</p>");
    $("#id_emergency_contact").next().css("font-size", "85%");

}
if($("#id_registration_no").length) {
    $("#id_registration_no").after("<p>eg: UP 15 D 1234</p>");
    $("#id_registration_no").next().css("font-size", "85%");
}
if($("#id_nickname").length) {
    $("#id_nickname").after("<p>eg: B3</p>");
    $("#id_nickname").next().css("font-size", "85%");
}
$(":checkbox").css({"float": "left", "clear": "both", "margin-top": "-25px",});