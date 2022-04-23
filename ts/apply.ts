import highlightNav from "./lib/nav";
import startMsg from "./lib/startMessage";
import registerModalClosers from "./lib/registerModalClosers";
import registerModalOpeners from "./lib/registerModalOpeners";
import { RadioGroup } from "./lib/radio";
import { Form } from "./lib/form";
import { GraphQLClient } from "./lib/api/executor";
import { Modal } from "./lib/modal";

startMsg();

function mapToBool(yn: string): boolean {
	if (!["Yes", "No"].includes(yn)) throw new Error("invalid data");

	return yn == "Yes";
}

window.addEventListener("DOMContentLoaded", () => {
	highlightNav();
	registerModalClosers();
	registerModalOpeners();

	const form = new Form("editor-form");
	const discordTag = form.getInput("discord-tag");
	const radioGroup = new RadioGroup("can-add-games");
	const radioGroup2 = new RadioGroup("can-expand-audience");
	const anythingElse = form.getInput("anything-else");
	const graphql = new GraphQLClient();

	discordTag.addValidator(data => {
		if (data.search(/.+#\d{4}$/) || data.length > 150) {
			return {
				success: false,
				message: "Invalid tag",
			};
		}

		return { success: true };
	});

	[radioGroup, radioGroup2].forEach(group => {
		form.addValidator(() => {
			try {
				group.getValue();

				return { success: true };
			} catch {
				return {
					success: false,
					message: "This is required",
				};
			}
		}, group.root.querySelector("small")!);
	});

	anythingElse.addValidator(data => {
		if (data.length > 1000) {
			return {
				success: false,
				message: "Cannot exceed 1000 characters",
			};
		}

		return { success: true };
	});

	form.setCallback((_, data) => {
		console.log(radioGroup.getValue());
		const promise = graphql.apply(
			data["discord-tag"],
			mapToBool(radioGroup.getValue()),
			mapToBool(radioGroup2.getValue()),
			data["anything-else"]
		);

		promise.then(() => window.location.reload());
	});
});
