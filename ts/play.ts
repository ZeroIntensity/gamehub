import startMsg from "./lib/startMessage";

startMsg();

window.addEventListener("DOMContentLoaded", () => {
	const frame = document.getElementById("frame")!;
	const spinner = document.getElementById("spinner")!;

	frame.addEventListener("load", () => {
		spinner.classList.add("hidden");
		frame.classList.remove("hidden");
	});
});
