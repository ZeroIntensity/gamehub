import highlightNav from "./lib/nav";
import handleEpoch from "./lib/handleEpoch";
import registerModalClosers from "./lib/registerModalClosers";
import getComments from "./lib/comments";
import { Modal } from "./lib/modal";
import { Form } from "./lib/form";
import noMatch from "./lib/utils/noMatch";
import createComment from "./lib/comment";
import { Comment } from "./lib/api/schema";
import handleErrors from "./lib/utils/handleErrors";

function addComment(
    list: HTMLElement,
    comment: { author: string; epoch: number; content: string } & Comment
) {
    const item = document.createElement("li");
    item.classList.add("p-2");
    item.innerHTML = `<div
                                        class="text-white bg-zinc-700 rounded-lg p-2"
                                    >
                                        <div class="flex">
                                            <p class="font-semibold">
                                                ${comment.author}
                                            </p>
                                            <p
                                                data-type="epoch"
                                                class="font-semibold pl-3 text-zinc-500"
                                            >${comment.epoch}</p>
                                        </div>
                                        <p class="font-thin text-zinc-400">
                                            ${comment.content}
                                        </p>
                                    </div>`;
    list.appendChild(item);
    handleEpoch();
}

window.addEventListener("DOMContentLoaded", () => {
    highlightNav();
    handleEpoch();
    registerModalClosers();

    const commentOpeners = document.querySelectorAll(
        '[data-type="opencomments"]'
    );

    commentOpeners.forEach(element => {
        const gameName = element.getAttribute("data-game-name")!;
        const modal = new Modal("comment-modal");
        let formShowed = false;
        let form: Form;

        if (document.getElementById("comment-form")) {
            formShowed = true;
            form = new Form("comment-form");
            const commentInput = form.getInput("comment-content");

            commentInput.addValidator(data => {
                if (data.length > 300) {
                    return {
                        success: false,
                        message:
                            "Comment content cannot exceed 300 characters.",
                    };
                }

                if (!noMatch(data, /<.*>/g)) {
                    return {
                        success: false,
                        message: "Invalid comment.",
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
        }

        (<HTMLElement>element).onclick = () => {
            const list = <HTMLUListElement>(
                document.getElementById("commentBody")!
            );
            list.innerHTML = "";

            const comments = getComments(gameName);
            comments.then(data => {
                if (!data.length) {
                    list.innerHTML = `<div class="text-center p-4">
                                    <p class="text-white font-semibold text-lg lg:text-md">
                                        No Comments
                                    </p>
                                    <p class="text-zinc-400 font-thin text-md lg:text-sm">
                                        Be the first to make a comment.
                                    </p>
                                </div>`;
                }

                data.forEach(comment => addComment(list, comment));
            });

            if (formShowed) {
                form.setCallback(
                    (_: SubmitEvent, inputData: Record<string, string>) => {
                        const resp = createComment(
                            gameName,
                            inputData["comment-content"]
                        );
                        resp.then(data => {
                            let handled: WrapperResponse;

                            try {
                                handled = handleErrors(data);
                            } catch (e) {
                                form.error("Something went wrong.");
                                throw e;
                            }

                            if (!handled.ok) {
                                form.error(`Server error: ${handled.message!}`);
                            } else
                                addComment(list, data.json.data!.createComment);
                        });

                        resp.catch(err => {
                            console.error(`Failed to post comment: ${err}`);
                        });
                    }
                );
            }

            modal.open();
        };
    });
});
