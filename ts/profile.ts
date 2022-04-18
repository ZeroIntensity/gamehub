import highlightNav from "./lib/nav";
import startMsg from "./lib/startMessage";
import handleEpoch from "./lib/handleEpoch";
import registerModalClosers from "./lib/registerModalClosers";
import { Modal } from "./lib/modal";

startMsg();

window.addEventListener("DOMContentLoaded", () => {
	highlightNav();
	handleEpoch();
	registerModalClosers();

	const modal = new Modal("report-modal");
});

declare let window: ExtendedWindow;

window.openReportModal = () => {
	const modal = new Modal("report-modal");
	modal.open();
};
