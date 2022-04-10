import { Form } from "../form";

export default (
    resp: Promise<WrapperResponse>,
    form: Form,
    callback: () => void = () => {}
) => {
    resp.then(data => {
        if (!data.ok) {
            form.error(`Server error: ${data.message!}`);
        } else callback();
    });

    resp.catch(_ => {
        form.error("Something went wrong.");
    });
};
