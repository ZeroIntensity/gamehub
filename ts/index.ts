import highlightNav from "./lib/nav";
import { Modal } from "./lib/modal";
import { createPost } from "./lib/post";
import { Form } from "./lib/form";
import noMatch from "./lib/utils/noMatch";
import handleEpoch from "./lib/handleEpoch";
import registerModalClosers from "./lib/registerModalClosers";
import formResponse from "./lib/utils/formResponse";

window.addEventListener("DOMContentLoaded", () => {
    highlightNav();
    handleEpoch();
    registerModalClosers();

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
                message: "Invalid title.",
            };
        }

        if (!data) {
            return {
                success: false,
                message: "Title is required.",
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
                message: "Cannot be more than 300 characters.",
            };
        }

        if (!noMatch(data, /<.*>/g)) {
            return {
                success: false,
                message: "Invalid content.",
            };
        }

        if (!data) {
            return {
                success: false,
                message: "Content is required.",
            };
        }

        return {
            success: true,
        };
    });

    form.setCallback((_, data) => {
        const resp = createPost(data["post-title"], data["post-content"]);
        formResponse(resp, form, window.location.reload);
    });
});

declare let window: ExtendedWindow;

window.createPostModal = () => {
    let modal = new Modal("post-modal");
    modal.open();
};
