import { Modal } from "./modal";

export default () => {
	const modalOpeners = document.querySelectorAll('[data-type="modalopen"]');

	modalOpeners.forEach(element => {
		const target = element.getAttribute("data-target")!;
		const modal = new Modal(target);

		(element as HTMLElement).onclick = () => modal.open();
	});
};
