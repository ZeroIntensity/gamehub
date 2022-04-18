import highlightNav from "./lib/nav";
import startMsg from "./lib/startMessage";
import handleEpoch from "./lib/handleEpoch";
import registerModalClosers from "./lib/registerModalClosers";
import { Modal } from "./lib/modal";
import { Form } from "./lib/form";
import { GraphQLClient } from "./lib/api/executor";
import handleFormPromise from "./lib/utils/handleFormPromise";

startMsg();

window.addEventListener("DOMContentLoaded", () => {
	highlightNav();
	handleEpoch();
	registerModalClosers();

	const graphql = new GraphQLClient();
	const form = new Form("report-form");
	const reason = form.getInput("report-reason");
	const username = form.element.getAttribute("data-user-name")!;

	reason.addValidator(data => {
		if (data.length > 300) {
			return {
				success: false,
				message: "Cannot exceed 300 characters.",
			};
		}

		return { success: true };
	});

	form.setCallback((_, data) => {
		const promise = graphql.userReport(data["report-reason"], username);
		handleFormPromise(promise, form, () => window.location.reload());
	});
});

declare let window: ExtendedWindow;

window.openReportModal = () => {
	const modal = new Modal("report-modal");
	modal.open();
};

window.terminateModal = () => {
	const modal = new Modal("terminate-modal");
	modal.open();
};
