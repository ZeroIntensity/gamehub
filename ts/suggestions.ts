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

	const form = new Form("suggestion-form");
	const input = form.getInput("suggestion-content");
	const graphql = new GraphQLClient();

	input.addValidator(data => {
		if (data.length > 300) {
			return {
				success: false,
				message: "Cannot exceed 300 characters.",
			};
		}

		return { success: true };
	});

	form.setCallback((_, data) => {
		const promise = graphql.suggest(data["suggestion-content"]);
		handleFormPromise(promise, form, () => window.location.reload());
	});
});
