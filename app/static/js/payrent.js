$(function() {
	function postAndRedirect(url, postData) {
	    var postFormStr = "<form method='POST' action='" + url + "'>\n";

	    for (var key in postData) {
	        if (postData.hasOwnProperty(key)) {
	            postFormStr += "<input type='hidden' name='" + key + "' value='" + postData[key] + "'></input>";
	        }
	    }

	    postFormStr += "</form>";

	    var formElement = $(postFormStr);

	    $('body').append(formElement);
	    $(formElement).submit();
	}

	var handler = StripeCheckout.configure({
		key: 'pk_test_sCKWz16ZwHzNJD0QI8b9EUfF',
		token: function(token) {
		  // Use the token to create the charge with a server-side script.
		  // You can access the token ID with `token.id`

		  var email = token.email;

		  postAndRedirect("/charge", {
		  	stripeToken: token.id,
		  	amount: document.getElementById("amount").value,
		  	type: token.type,
		  	email: email
		  });
		}
	});

	$('#customButton').on('click', function(e) {
		// Open Checkout with further options
		/*var email = document.getElementById("email").innerHTML;
		var elems = email.split("@");
		email = elems[0] + "+fill_now@" + elems[1];
		console.log("New email: " + email);*/

		handler.open({
			name: document.getElementById('property_name').innerHTML,
			description: 'Make a payment',
			amount: Math.round(parseFloat(document.getElementById("amount").value)*100),
			email: document.getElementById("email").innerHTML,
			zipCode: true,
			bitcoin: false
		});
		e.preventDefault();
	});

	// Close Checkout on page navigation
	$(window).on('popstate', function() {
	handler.close();
	});
});
