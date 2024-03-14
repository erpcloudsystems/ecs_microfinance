// Copyright (c) 2023, erpcloudsystems and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Employee Insurance Data"] = {
	"filters": [
		{
			fieldname: 'name',
			label: __('Employee'),
			fieldtype: 'Link',
			Options: "Employee",
		  },
	
		  

	]
};

	// Function to convert English numbers to Arabic

	$(document).ready(function() {
		// Function to convert English numbers to Arabic
		console.log("Converting English to Arabic");

		function englishToArabic(number) {
			const arabicDigits = ["٠", "١", "٢", "٣", "٤", "٥", "٦", "٧", "٨", "٩"];
			return String(number).replace(/\d/g, digit => arabicDigits[digit]);
		}

		// Loop through each element with class 'english-to-arabic' and convert the text
		$(".english-to-arabic").each(function() {
			var englishText = $(this).text();
			var englishNumber = parseFloat(englishText); // Convert text to number
			var arabicText = englishToArabic(englishNumber);
			$(this).text(arabicText);
		});
	});

	function convertToArabic(number) {
		var arabicNumerals = ["٠", "١", "٢", "٣", "٤", "٥", "٦", "٧", "٨", "٩"];
		var arabicNumber = "";
		for (var i = 0; i < number.length; i++) {
			arabicNumber += arabicNumerals[number.charAt(i)];
		}
		return arabicNumber;
	}
