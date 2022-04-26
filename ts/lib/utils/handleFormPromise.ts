import { Form } from "../form";
import { isAuthenticated } from "../cookies";

export default <T>(
	promise: Promise<APIResponse<T>>,
	form: Form,
	callback: Function
) => {
	promise.then(response => {
		if (response.ok) {
			return callback();
		}

		form.error(response.message!);
	});
	promise.catch(error => {
		if (
			error.message == "GraphQL request failed: Invalid username or password."
		)
			if (!isAuthenticated) window.location.href = "/login";
			else form.error(`Internal error: ${error.message}`);
	});
};
