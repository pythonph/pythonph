function viewOfficerList() {
	var list = $('#view-list ul');
	var button = $('#view-more');

	var numInList = list.length;
	var numToShow = 1;

	list.hide();

	if (numInList > numToShow) {
		button.show();
	}

	if (!isMobileDevice() || !button.filter(':visible').length) {
		numToShow = numInList;
	} else {
		numToShow = 1;
	}

	list.slice(0, numToShow).show();

	button.click(function () {
		var showing = list.filter(':visible').length;

		list.slice(showing - 1, showing + numToShow).fadeIn();

		var nowShowing = list.filter(':visible').length;

		if (nowShowing >= numInList) {
			button.hide();
		}
	});
}

function isMobileDevice() {
	if (window.matchMedia('(max-width: 767px)').matches) {
		return true;
	}

	return false;
}

window.onresize = function () {
	viewOfficerList();
};

window.addEventListener('DOMContentLoaded', function () {
	viewOfficerList();

	document.body.classList.remove('preload');

	AOS.init({
		delay: 230,
		duration: 1000,
		easing: 'py-easing',
		offset: 50,
		once: true,
		startEvent: 'DOMContentLoaded',
	});
});

document.querySelector('.btn-toggle').addEventListener('click', function () {
	var slider = document.querySelector('.slider-pane');
	var body = document.body;

	if (!slider.classList.contains('opened')) {
		this.classList.add('opened');
		slider.classList.add('opened');
		body.classList.add('overflow-hidden');
	} else {
		this.classList.remove('opened');
		slider.classList.remove('opened');
		body.classList.remove('overflow-hidden');
	}
});

var swiper = new Swiper('.carousel-swiper', {
	pagination: {
		el: '.carousel-pagination',
		clickable: true,
	},
	loop: true,
});

var tooltipTriggerList = [].slice.call(
	document.querySelectorAll('[data-bs-toggle="tooltip"]')
);

var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
	return new bootstrap.Tooltip(tooltipTriggerEl);
});
