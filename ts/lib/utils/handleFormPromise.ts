import { Form } from "../form";

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
		form.error(`Internal error: ${error.message}`);
	});
};
