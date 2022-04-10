import highlightNav from "./lib/nav";
import handleEpoch from "./lib/handleEpoch";
import registerModalClosers from "./lib/registerModalClosers";
import getComments from "./lib/comments";
import { Modal } from "./lib/modal";

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

        (<HTMLElement>element).onclick = () => {
            const list = <HTMLUListElement>(
                document.getElementById("commentBody")!
            );
            const comments = getComments(gameName);

            comments.then(data => {
                data.forEach(comment => {
                    const item = document.createElement("li");
                    item.innerHTML = comment.content;
                    list.appendChild(item);
                });
            });
            modal.open();
        };
    });
});
