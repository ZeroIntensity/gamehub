import highlightNav from "./lib/nav";
import handleEpoch from "./lib/handleEpoch";
import registerModalClosers from "./lib/registerModalClosers";
import { Modal } from "./lib/modal";
import { Form, BaseForm } from "./lib/form";
import noMatch from "./lib/utils/noMatch";
import { Comment } from "./lib/api/schema";
import { GraphQLClient } from "./lib/api/executor";
import startMsg from "./lib/startMessage";
import { isAuthenticated } from "./lib/cookies";
import hasAccess from "./lib/utils/hasAccess";
import registerModalOpeners from "./lib/registerModalOpeners";
import handleFormPromise from "./lib/utils/handleFormPromise";

startMsg();

declare let window: ExtendedWindow;
const graphql = new GraphQLClient();

function validateComment(data: string): ValidatorResponse {
	if (data.length > 300) {
		return {
			success: false,
			message: "Comment content cannot exceed 300 characters.",
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
}

function loadComments(list: HTMLElement, gameName: string) {
	list.innerHTML = `<svg
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

	const comments = graphql.getComments(gameName);

	comments.then(resp => {
		const data = resp.response.json.data!.getGame.comments;
		list.innerHTML = !data.length
			? `<div class="text-center p-4" id="nocom">
                                    <p class="text-white font-semibold text-lg lg:text-md">
                                        No Comments
                                    </p>
                                    <p class="text-zinc-400 font-thin text-md lg:text-sm">
                                        Be the first to make a comment.
                                    </p>
                                </div>`
			: "";

		const len = document.querySelector(
			`[data-type="commentlen"][data-game-name="${gameName}"]`
		)!;

		len.innerHTML = String(data.length);

		data.forEach(comment => {
			addComment(list, gameName, comment);
		});
		registerDeletes();
		registerEditors();
	});
}

function registerDeletes() {
	const buttons: NodeListOf<HTMLElement> = document.querySelectorAll(
		'[data-type="deletebutton"]'
	);

	buttons.forEach(btn => {
		const gameName = btn.getAttribute("data-game-name")!;
		const id = btn.getAttribute("data-comment-id")!;

		btn.onclick = () => {
			const promise = graphql.deleteComment(gameName, id);

			promise.then(_ => {
				loadComments(document.getElementById("commentBody")!, gameName);
			});
		};
	});
}

function registerEditors() {
	const buttons: NodeListOf<HTMLElement> = document.querySelectorAll(
		'[data-type="editbutton"]'
	);

	buttons.forEach(btn => {
		const gameName = btn.getAttribute("data-game-name")!;
		const id = btn.getAttribute("data-comment-id")!;

		const content: HTMLElement = document.querySelector(
			`[data-type="commentcontent"][data-comment-id="${id}"]`
		)!;
		const form = new BaseForm(
			document.querySelector(`[id="editForm"][data-comment-id="${id}"]`)!
		);
		const input = form.getInput("edit-content");
		input.addValidator(data => validateComment(data));

		const finalizeEdit = <T>(
			promise: Promise<APIResponse<T>>,
			inputContent: string
		) => {
			handleFormPromise(promise, form, () => {});
			content.classList.remove("hidden");
			content.innerHTML = inputContent;
			form.element.classList.add("hidden");
		};

		form.setCallback((_, data) => {
			let inputContent = data["edit-content"];
			const promise = graphql.editComment(inputContent, gameName, id);

			finalizeEdit(promise, inputContent);
		});

		btn.onclick = () => {
			if (content.classList.contains("hidden")) {
				let value: string = input.element.value;

				// form.submit isnt using the callback for some reason, so i have to do this manually
				form.fireValidators();
				const promise = graphql.editComment(value, gameName, id);
				finalizeEdit(promise, value);
			} else {
				input.element.value = content.innerHTML;
				content.classList.add("hidden");
				form.element.classList.remove("hidden");
			}

			// TODO: optimize
		};
	});
}

function addComment(
	list: HTMLElement,
	gameName: string,
	comment: {
		id: string;
		author: string;
		epoch: number;
		content: string;
		accountType: AccountType;
	} & Comment,
	scroll: boolean = false
) {
	const username: string = document.body.getAttribute("data-user-name")!;
	const accountType: AccountType = <AccountType>(
		document.body.getAttribute("data-account-type")!
	);
	let item = document.createElement("li");
	item.classList.add("p-2");

	let svg: string = "";

	if (comment.accountType != "user") {
		svg =
			comment.accountType == "developer"
				? `<svg
					xmlns="http://www.w3.org/2000/svg"
					class="h-6 w-6"
					fill="none"
					viewBox="0 0 24 24"
					stroke="currentColor"
					stroke-width="2"
				>
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						d="M8 9l3 3-3 3m5 0h3M5 20h14a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
					/>
				</svg>`
				: `<svg
					xmlns="http://www.w3.org/2000/svg"
					class="h-6 w-6"
					fill="none"
					viewBox="0 0 24 24"
					stroke="currentColor"
					stroke-width="2"
				>
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"
					/>
				</svg>`;
	}

	let editBtn: string =
		username == comment.author
			? `<svg
		xmlns="http://www.w3.org/2000/svg"
		class="h-6 w-6 text-zinc-400 hover:text-zinc-300 transition-all"
		fill="none"
		viewBox="0 0 24 24"
		stroke="currentColor"
		stroke-width="2"
		data-type="editbutton"
		data-comment-id="${comment.id}"
		data-game-name="${gameName}"
	>
		<path
			stroke-linecap="round"
			stroke-linejoin="round"
			d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"
		/>
	</svg>`
			: "";

	let deleteBtn: string = hasAccess(accountType, comment.accountType)
		? `<svg
	xmlns="http://www.w3.org/2000/svg"
	class="h-6 w-6 text-zinc-400 hover:text-zinc-300 transition-all"
	fill="none"
	viewBox="0 0 24 24"
	stroke="currentColor"
	stroke-width="2"
	data-type="deletebutton"
	data-comment-id="${comment.id}"
	data-game-name="${gameName}"
>
	<path
		stroke-linecap="round"
		stroke-linejoin="round"
		d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
	/>
</svg>`
		: "";

	item.innerHTML = `<div>
	<div
		class="text-white bg-zinc-700 rounded-lg p-2 break-words flex"
	>
		<div>
			<div class="flex">
				<div class="space-x-1 flex">
					${svg}
					<a
						href="/profile/${comment.author}"
						class="font-semibold hover:opacity-50 transition-all"
						>${comment.author}</a
					>
				</div>
				<p
					data-type="epoch"
					class="font-semibold pl-3 text-zinc-500"
				>
					${comment.epoch}
				</p>
			</div>
			<p class="font-thin text-zinc-400" data-type="commentcontent" data-comment-id="${
				comment.id
			}">${comment.content}</p>
			${
				comment.author == username
					? `
			<small></small>
			<form class="hidden" id="editForm" data-comment-id="${comment.id}">
				<div class="flex h-fit">
					<div class="w-full">
						<input
							type="text"
							name="edit-content"
							id="edit-content"
							placeholder="balls..."
							class="bg-zinc-600 w-full text-md lg:text-sm rounded-lg p-2.5 text-white focus:outline-none"
						/>
						<small class="z-20"></small>
					</div>
				</div>
			</form>
			`
					: ""
			}
		</div>
		<div
			data-comment-id="${comment.id}"
			class="self-center ml-auto flex space-x-2"
		>
			${deleteBtn}
			${editBtn}
		</div>
	</div>
</div>`;

	list.appendChild(item);
	if (scroll) item.scrollIntoView();
	handleEpoch();
}

window.addEventListener("DOMContentLoaded", () => {
	highlightNav();
	handleEpoch();
	registerModalClosers();
	registerModalOpeners();

	const commentOpeners = document.querySelectorAll(
		'[data-type="opencomments"]'
	);

	if (document.getElementById("comment-form")) {
		var formShowed = true;
		var form = new Form("comment-form");
		const commentInput = form.getInput("comment-content");

		commentInput.addValidator(data => validateComment(data));
	}

	const modal = new Modal("comment-modal");

	commentOpeners.forEach(element => {
		const gameName = element.getAttribute("data-game-name")!;

		(<HTMLElement>element).onclick = () => {
			const list = <HTMLUListElement>document.getElementById("commentBody")!;
			loadComments(list, gameName);
			registerEditors();

			if (formShowed) {
				form.setCallback(
					(_: SubmitEvent, inputData: Record<string, string>) => {
						form.element.querySelector("small")!.innerHTML = `<svg
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
						const resp = graphql.createComment(
							gameName,
							inputData["comment-content"]
						);

						resp.then(data => {
							if (!data.ok) {
								return form.error(data.message!);
							}

							addComment(
								list,
								gameName,
								data.response.json.data!.createComment,
								true
							);
							loadComments(list, gameName);

							form.clear();
						});

						resp.catch(err => console.error(`Failed to post comment: ${err}`));
					},
					true
				);
			}

			modal.open();
		};
		const gameForm = new Form("game-form");

		const gameTitle = gameForm.getInput("game-title");
		const url = gameForm.getInput("game-url");

		gameTitle.addValidator(data => {
			if (!data) {
				return {
					success: false,
					message: "Name is required.",
				};
			}

			return { success: true };
		});

		url.addValidator(data => {
			if (!data) {
				return {
					success: false,
					message: "URL is required.",
				};
			}

			return { success: true };
		});

		gameForm.setCallback((_, data) => {
			const promise = graphql.addGame(data["game-title"], data["game-url"]);
			handleFormPromise(promise, form, () => window.location.reload());
		});
	});

	const likeButtons = document.querySelectorAll('[data-type="likebutton"]');

	likeButtons.forEach(element => {
		const gameName: string = element.getAttribute("data-game-name")!;
		const count = element.querySelector("p")!;

		(element as HTMLElement).onclick = () => {
			if (!isAuthenticated)
				return (function () {
					window.location.href = "/login";
				})(); // this is to make sure that the code below doesnt get run

			const isLiked = document
				.querySelector(`[data-type="likebutton"][data-game-name="${gameName}"`)! // the attribute is cached when using element
				.getAttribute("data-liked");

			if (isLiked == "True") {
				count.innerHTML = String(Number(count.innerHTML) - 1);
				element.classList.remove("text-rose-500", "hover:text-rose-400");
				element.classList.add("text-zinc-400", "hover:text-zinc-300");
				element.setAttribute("data-liked", "False");
				graphql.unlikeGame(gameName);
			} else {
				count.innerHTML = String(Number(count.innerHTML) + 1);
				element.classList.add("text-rose-500", "hover:text-rose-400");
				element.classList.remove("text-zinc-400", "hover:text-zinc-300");
				element.setAttribute("data-liked", "True");
				graphql.likeGame(gameName);
			}
			// not sure if theres a better way to do this
		};
	});

	const deleteButtons = document.querySelectorAll('[data-type="deletemodal"]');

	deleteButtons.forEach(element => {
		const gameName: string = element.getAttribute("data-game-name")!;
		const modal = new Modal("delete-modal");

		(element as HTMLElement).onclick = () => {
			modal.open();

			window.deleteGame = () => {
				const promise = graphql.deleteGame(gameName);
				promise.then(_ => window.location.reload());
			};
		};
	});
});
