import highlightNav from "./lib/nav";
import startMsg from "./lib/startMessage";
import { Form } from "./lib/form";
import { GraphQLClient } from "./lib/api/executor";
import handleFormPromise from "./lib/utils/handleFormPromise";
import noMatch from "./lib/utils/noMatch";

startMsg();

window.addEventListener("DOMContentLoaded", () => {
	highlightNav();

	const login = new Form("login-form");
	const signup = new Form("signup-form");
	const graphql = new GraphQLClient();

	login.setCallback((_, data) => {
		const response = graphql.login(
			data["login-username"],
			data["login-password"]
		);

		handleFormPromise(response, login, () => window.location.reload());
	});

	const usernameInput = signup.getInput("signup-username");
	const passwordInput = signup.getInput("signup-password");

	usernameInput.addValidator(data => {
		if (data.length < 4)
			return { success: false, message: "Must be at least 4 characters" };

		if (data.length > 20)
			return { success: false, message: "Cannot exceed 20 characters" };

		if (!noMatch(data, /.*(<|>|\(|\)|\*|&|@|\'|\"|,|\{|\}|\[|\]| ).*/)) {
			return {
				success: false,
				message: "Cannot contain any special characters",
			};
		}
		return { success: true };
	});

	passwordInput.addValidator(data => {
		if (data.length < 6)
			return { success: false, message: "Must be at least 6 characters" };

		return { success: true };
	});

	signup.setCallback((_, data) => {
		const username: string = data["signup-username"];
		const password: string = data["signup-password"];

		const firstRes = graphql.createAccount(username, password);
		signup.element.querySelector("small")!.innerHTML = `<svg
		role="status"
		class="p-3 mr-2 w-14 h-14 text-zinc-700 animate-spin fill-orange-400"
		viewBox="0 0 100 101"
		fill="none"
		xmlns="http://www.w3.org/2000/svg"
	>
		<path
			d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
			fill="currentColor"
		/>
		<path
			d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
			fill="currentFill"
		/>
	</svg>`;

		firstRes.catch(err => {
			signup.error(`Internal error: ${err.message}`);
		});

		firstRes.then(data => {
			if (!data.ok) return signup.error(`${data.message!}`);
			const nextRes = graphql.login(username, password);
			handleFormPromise(nextRes, signup, () => (window.location.href = "/"));
		});
	});
});
