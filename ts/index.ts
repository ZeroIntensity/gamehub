import highlightNav from "./lib/nav";
import { Modal } from "./lib/modal";
import { createPost } from "./lib/post";
import { Form } from "./lib/form";
import noMatch from "./lib/utils/noMatch";

window.addEventListener("DOMContentLoaded", () => {
    const elements = document.querySelectorAll('[data-type="epoch"]');

    elements.forEach(element => {
        const epoch = Number(element.innerHTML);
        const date = new Date(epoch * 1000);
        const month = date.toLocaleString("default", { month: "long" });

        (element as HTMLElement).style.display = "block";
        element.innerHTML = `${month} ${date.getUTCDate()}, ${date.getUTCFullYear()}`;
    });

    highlightNav();

    const modalClosers = document.querySelectorAll('[data-type="modalclose"]');

    modalClosers.forEach(element => {
        const origin = <HTMLElement>element;
        let parent: HTMLElement = origin;

        for (let i = 0; i < 10; i++) {
            if (parent.getAttribute("data-type") == "modal") break;
            parent = parent.parentElement!;
        }

        origin.onclick = () => {
            parent.classList.add("hidden");
        };
    });

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
        resp.then(data => {
            if (!data.ok) {
                form.error(`Server error: ${data.message!}`);
            } else window.location.reload();
        });

        resp.catch(_ => {
            form.error("Something went wrong.");
        });
    });
});

declare let window: ExtendedWindow;

window.createPostModal = () => {
    let modal = new Modal("post-modal");
    modal.open();
};
