$(document).ready(function() {
});

$(document).on("click", "#login_button", function() {
	var username = $("#bitsID").val();
	var password = $("#password").val();
	var validation = false;

    if(username.match(/^[a-zA-Z0-9]{11}$/)) {
        $("#bitsIDdiv").removeClass("has-error");
    } else {
        $("#bitsIDdiv").addClass("has-error");
	    event.preventDefault();
    }
});

$(document).on("click", "#addOption1", function() {
	var optionTable = $("#optionTable");
	var selector = $("#optionTable tr:last");
	var newElement = selector.clone(true);
	
	
	$(selector).after(newElement);
	
});

$(document).on("click", "#addOption", function() {
	var optionTable = $("#optionTable");
	
	var optionIndex = -1;
	
	$('#optionTable .option-row').each(function (i, row) {
		optionIndex++;
	});
	
	++optionIndex;
	
	jQuery("<tr />", {
		"class": "option-row"
	})
		.append(jQuery("<td />")
			.append(jQuery("<div />", {
		        "class":"col-md-4"
			})
				.append(jQuery("<input />", {
					"id": "id_option_set-" + optionIndex + "-option_text",
					"name": "option_set-" + optionIndex + "-option_text",
					"type": "text",
					"class": "form-control"
				}))
				.append(jQuery("<input />", {
					"id": "id_option_set-" + optionIndex + "-id",
					"name": "option_set-" + optionIndex + "-id",
					"type": "hidden",
					"class": "form-control",
					"value": ""
				}))
				.append(jQuery("<input />", {
					"id": "id_option_set-" + optionIndex + "-order",
					"name": "option_set-" + optionIndex + "-order",
					"type": "hidden",
					"class": "form-control",
					"value": "" + (optionIndex + 1)
				}))
				/*
				.append(jQuery("<input />", {
					"id": "id_option_set-" + optionIndex + "-question",
					"name": "option_set-" + optionIndex + "-question",
					"type": "hidden",
					"class": "form-control",
					"value": "" + question_id
				}))
				*/
			)
			.append(jQuery("<div />", {
		        "class":"col-md-2 pull-right"
			})
				.append(jQuery("<button />", {
					"id": "deleteOption",
			        "class":"btn btn-link",
			        "type": "button",
			        html: "<span class='glyphicon glyphicon-remove'></span>"
				}))
			)
				
		)
	.appendTo(optionTable);
	
	var total = 0
	$('#optionTable .option-row').each(function (i, row) {
		total++;
	});
	
	$('#id_option_set-TOTAL_FORMS').val(total);
});

$(document).on("click", "#deleteOption", function() {
	var item = $( this );
	var parentRow = $(this.parentElement.parentElement);
	parentRow.remove();

	var a = $('#id_option_set-TOTAL_FORMS').val();
	var total = 0;
	$('#optionTable .option-row').each(function (i, row) {
		total++;
	});
	
	$('#id_option_set-TOTAL_FORMS').val(total);
});
