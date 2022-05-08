import moment from "moment";

export default () => {
	const elements = document.querySelectorAll('[data-type="epoch"]');

	elements.forEach(element => {
		const epoch = Number(element.innerHTML);
		if (isNaN(epoch)) return;

		(element as HTMLElement).style.display = "block";
		element.innerHTML = moment.unix(epoch).fromNow();
	});
};
