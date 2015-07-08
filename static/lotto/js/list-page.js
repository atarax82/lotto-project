$(function() {
	var $checkTicketsButton = $('#check-tickets');
	var $ticketsTable = $('#ticket-list-wrapper');

	var loading = false;
	$checkTicketsButton.on('click', function() {
		if (loading) {
			return;
		}
		loading = true;
		
		$ticketsTable.find('table').replaceWith(
				'<p class="loading-text">Loading...</p>');

		// upcoming variable is set in the HTML template
		$ticketsTable.load('/ticket/ajax/check?upcoming='+upcoming, function() {
			loading = false;
		});
	});

});
