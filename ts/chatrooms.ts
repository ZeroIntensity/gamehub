import highlightNav from "./lib/nav";
import startMsg from "./lib/startMessage";
import { Modal } from "./lib/modal";
import { isAuthenticated } from "./lib/cookies";
import { Form, Input } from "./lib/form";
import registerModalClosers from "./lib/registerModalClosers";
import registerModalOpeners from "./lib/registerModalOpeners";
import handleFormPromise from "./lib/utils/handleFormPromise";
import { GraphQLClient } from "./lib/api/executor";

startMsg();

declare let window: ExtendedWindow;

function roomConnect(roomName: string, form: Form, input: Input) {
	const modal = new Modal("chatroom-modal");
	const roomContent = document.getElementById("room-content")!;
	const exit = document.getElementById("exitroom")!;
	let closed = false;

	modal.open();

	const protocol = window.location.protocol == "http:" ? "ws:" : "wss:";
	const ws = new WebSocket(
		`${protocol}//${window.location.host}/chatrooms/${roomName}/connect`
	);

	ws.onopen = () => {
		roomContent.innerHTML = "";
	};

	ws.onmessage = event => {
		const parse: RoomMessage = JSON.parse(event.data);
		const element = document.createElement("div");

		if (parse.author != "sys") {
			element.classList.add("pt-2");
			element.innerHTML = `
		<div
			class="text-white bg-zinc-700 rounded-lg p-2 break-words flex"
		>
			<div>
				<a
				href="/profile/${parse.author}"
				class="font-semibold hover:opacity-50 transition-all"
				>${parse.author}</a
			>
				<p class="font-thin text-zinc-400" data-type="commentcontent">${parse.message}</p>
			</div>
		</div>`;
		} else {
			element.classList.add("py-1");
			element.innerHTML = `<p class="text-zinc-400 font-thin">${parse.message}</p>`;
		}

		roomContent.appendChild(element);
	};

	ws.onerror = _ => {
		const element = document.createElement("div");
		element.classList.add("py-1");
		element.innerHTML = `<p class="text-rose-300 font-thin">An error occured.</p>`;

		roomContent.appendChild(element);
	};

	ws.onclose = event => {
		closed = true;
		if (event.code != 1005) {
			const element = document.createElement("div");
			element.classList.add("py-1");
			element.innerHTML = `<p class="text-rose-300 font-thin">Connection lost: Error ${
				event.code
			} ${event.code == 1008 ? "(are you opened in another tab?)" : ""}</p>`;

			roomContent.appendChild(element);
		} else
			roomContent.innerHTML = `<svg
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
	};

	form.setCallback((_, data) => {
		if (closed) form.error("Connection has been lost.");
		else ws.send(data["message-content"]);
	});

	exit.onclick = () => {
		modal.close();
		ws.close();
	};
}

window.addEventListener("DOMContentLoaded", () => {
	highlightNav();
	registerModalClosers();
	registerModalOpeners();

	const form = new Form("room-form");
	const input = form.getInput("room-name");
	const graphql = new GraphQLClient();

	input.addValidator(data => {
		if (!data) {
			return {
				success: false,
				message: "Name is required.",
			};
		}

		return { success: true };
	});

	form.setCallback((_, data) => {
		const promise = graphql.createRoom(data["room-name"]);
		handleFormPromise(promise, form, () => window.location.reload());
	});

	const joinButtons = document.querySelectorAll('[data-type="chatroomjoin"]');
	const messageForm = new Form("chatroom-form");
	const messageInput = messageForm.getInput("message-content");

	messageInput.addValidator(data => {
		if (!data) {
			return {
				success: false,
				message: "Message content is required.",
			};
		}

		if (data.length > 300) {
			return {
				success: false,
				message: "Cannot exceed 300 characters.",
			};
		}

		return { success: true };
	});

	joinButtons.forEach(element => {
		(element as HTMLElement).onclick = () => {
			if (!isAuthenticated) window.location.href = "/";
			else
				roomConnect(
					element.getAttribute("data-chatroom-name")!,
					messageForm,
					messageInput
				);
		};
	});

	const deleteButtons = document.querySelectorAll('[data-type="deletemodal"]');
	const deleteModal = new Modal("delete-modal");

	deleteButtons.forEach(element => {
		const roomName: string = element.getAttribute("data-chatroom-name")!;

		(element as HTMLElement).onclick = () => {
			deleteModal.open();

			window.deleteRoom = () => {
				const promise = graphql.deleteRoom(roomName);
				promise.then(_ => window.location.reload());
			};
		};
	});
});
