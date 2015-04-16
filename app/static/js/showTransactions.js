$(function() {
	var elements = document.getElementsByClassName('amount');

	for (var i = elements.length - 1; i >= 0; i--) {
		var amount = elements[i].innerHTML;
		amount = parseFloat(parseFloat(amount) / 100).toPercision(2);
		elements[i].innerHTML = '$'+amount.toString();

		if (isNaN(amount))
			elements[i].innerHTML = 'N/A';
	};

});
