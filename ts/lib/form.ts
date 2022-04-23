class Output {
	readonly targetElement: HTMLElement;

	constructor(element: HTMLElement) {
		this.targetElement = element;
	}

	protected displayMsg(message: string, type: "success" | "error"): void {
		this.targetElement.innerHTML = message;

		let a = type == "success" ? "text-emerald-400" : "text-rose-400";
		let b = type == "success" ? "text-rose-400" : "text-emerald-400";

		this.targetElement.classList.add(a);
		this.targetElement.classList.remove(b);
	}

	public error(message: string) {
		this.displayMsg(message, "error");
	}

	public success(message: string) {
		this.displayMsg(message, "success");
	}

	public clear() {
		this.displayMsg("", "error");
	}
}

export class Input extends Output {
	readonly element: HTMLInputElement;
	public validators: Array<Validator>;

	constructor(element: HTMLInputElement) {
		super(element.parentNode!.querySelector("small")!);
		this.element = element;
		this.validators = [];
	}

	public addValidator(callback: Validator) {
		this.validators.push(callback);
	}

	public data(): string {
		return this.element.value;
	}
}

export class Form extends Output {
	readonly element: HTMLFormElement;
	public inputs: Record<string, Input>;
	private submitCallback?: (
		event: SubmitEvent,
		data: Record<string, string>
	) => void;
	private manualClear: boolean = false;
	public validators: Array<{ callback: CustomValidator; hook: Output }> = [];

	constructor(id: string) {
		let element = <HTMLFormElement>document.getElementById(id)!;
		super(element.querySelector("small")!);

		this.element = element;
		this.inputs = {};

		Array.from(this.element.elements).forEach(item => {
			if (item.getAttribute("data-form-exclude")) return;
			this.inputs[item.id] = new Input(<HTMLInputElement>item);
		});

		this.element.addEventListener("submit", (event: SubmitEvent) => {
			event.preventDefault();
			let validated = true;

			Object.keys(this.inputs).forEach(input => {
				const obj = this.inputs[input];

				obj.validators.forEach(callback => {
					const response = callback(obj.element.value);

					if (!response.success) {
						obj.error(response.message!);
						validated = false;
					}
				});
			});

			this.validators.forEach(validator => {
				const response = validator.callback();

				if (!response.success) {
					validator.hook.error(response.message!);
					validated = false;
				}
			});

			if (!validated) return;
			if (!this.submitCallback) throw new Error("callback is not set");

			const data: Record<string, string> = {};

			Object.keys(this.inputs).forEach(
				key => (data[key] = this.inputs[key].data())
			);

			this.submitCallback(event, data);
			if (!this.manualClear) this.clear();
		});
	}

	public getInput(name: string): Input {
		if (!this.inputs.hasOwnProperty(name))
			throw new Error(`input "${name}" does not exist`);

		return this.inputs[name];
	}

	public setCallback(
		callback: (event: SubmitEvent, data: Record<string, string>) => void,
		manualClear: boolean = false
	): void {
		this.submitCallback = callback;
		this.manualClear = manualClear;
	}

	public clear() {
		Object.keys(this.inputs).forEach(key => {
			this.inputs[key].clear();
			this.inputs[key].element.value = "";
		});
		this.displayMsg("", "error");
	}

	public addValidator(callback: CustomValidator, hook: HTMLElement) {
		this.validators.push({ hook: new Output(hook), callback });
	}
}
