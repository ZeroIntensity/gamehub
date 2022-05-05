import highlightNav from "./lib/nav";
import startMsg from "./lib/startMessage";
import registerModalClosers from "./lib/registerModalClosers";
import registerModalOpeners from "./lib/registerModalOpeners";
import { Form } from "./lib/form";
import handleFormPromise from "./lib/utils/handleFormPromise";
import { GraphQLClient } from "./lib/api/executor";

startMsg();

window.addEventListener("DOMContentLoaded", () => {
	highlightNav();
	registerModalClosers();
	registerModalOpeners();

	const form = new Form("report-form");
	const reason = form.getInput("report-reason");

	const graphql = new GraphQLClient();

	reason.addValidator(data => {
		if (data.length > 300) {
			return {
				success: false,
				message: "Cannot exceed 300 characters",
			};
		}

		if (!data) {
			return {
				success: false,
				message: "Reason is required.",
			};
		}

		return { success: true };
	});

	form.setCallback((_, data) => {
		const promise = graphql.userReport(
			data["report-reason"],
			data["report-username"]
		);
		handleFormPromise(promise, form, () => window.location.reload());
	});

	const issueForm = new Form("issue-form");
	const content = issueForm.getInput("issue-content");
	const gameInput = issueForm.getInput("game-name");

	gameInput.addValidator(data => {
		if (!data) {
			return {
				success: false,
				message: "Game name is required.",
			};
		}

		return { success: true };
	});

	content.addValidator(data => {
		if (300 < data.length) {
			return {
				success: false,
				message: "Cannot exceed 300 characters.",
			};
		}

		if (!data) {
			return {
				success: false,
				message: "Content is required.",
			};
		}

		return { success: true };
	});

	issueForm.setCallback((_, data) => {
		const promise = graphql.issueReport(
			data["game-name"],
			data["issue-content"]
		);

		handleFormPromise(promise, issueForm, () => {
			window.location.reload();
		});
	});
});
