import highlightNav from "./lib/nav";
import { Modal } from "./lib/modal";
import { Form } from "./lib/form";
import noMatch from "./lib/utils/noMatch";
import handleEpoch from "./lib/handleEpoch";
import registerModalClosers from "./lib/registerModalClosers";
import { GraphQLClient } from "./lib/api/executor";
import startMsg from "./lib/startMessage";
import registerModalOpeners from "./lib/registerModalOpeners";

startMsg();

window.addEventListener("DOMContentLoaded", () => {
	highlightNav();
	handleEpoch();
	registerModalClosers();
	registerModalOpeners();

	const graphql = new GraphQLClient();
	const form = new Form("post-form");

	const titleInput = form.getInput("post-title");
	const contentInput = form.getInput("post-content");

	titleInput.addValidator(data => {
		if (data.length > 30) {
			return {
				success: false,
				message: "Cannot be more than 30 characters",
			};
		}

		if (!noMatch(data, /<.*>/g)) {
			return {
				success: false,
				message: "Invalid title",
			};
		}

		if (!data) {
			return {
				success: false,
				message: "Title is required",
			};
		}

		return {
			success: true,
		};
	});

	contentInput.addValidator(data => {
		if (data.length > 300) {
			return {
				success: false,
				message: "Cannot be more than 300 characters",
			};
		}

		if (!noMatch(data, /<.*>/g)) {
			return {
				success: false,
				message: "Invalid content",
			};
		}

		if (!data) {
			return {
				success: false,
				message: "Content is required",
			};
		}

		return {
			success: true,
		};
	});

	form.setCallback((_, data) => {
		const resp = graphql.createPost(data["post-title"], data["post-content"]);

		resp.then(data => {
			if (!data.ok) {
				form.error(data.message!);
			} else window.location.reload();
		});
	});
});
