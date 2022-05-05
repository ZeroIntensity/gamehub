class RadioButton {
	readonly element: HTMLElement;
	readonly id: string;
	public isSelected: boolean = false;
	private parent: RadioGroup;

	constructor(element: HTMLElement, parent: RadioGroup) {
		this.element = element;
		this.id = element.id;
		this.parent = parent;
	}

	private addRemove(
		addClasses: Array<string>,
		removeClasses: Array<string>
	): void {
		addClasses.forEach(className => this.element.classList.add(className));
		removeClasses.forEach(className =>
			this.element.classList.remove(className)
		);
	}

	public deselect() {
		if (this.isSelected) this.parent.selected = null;

		this.isSelected = false;
		this.addRemove(
			["bg-zinc-700", "text-zinc-400"],
			["bg-orange-400", "text-white"]
		);
	}

	public select() {
		this.parent.selected = this;
		this.isSelected = true;
		this.addRemove(
			["bg-orange-400", "text-white"],
			["bg-zinc-700", "text-zinc-400"]
		);
	}
}

export class RadioGroup {
	readonly buttons: Array<RadioButton>;
	readonly root: HTMLElement;
	private locked: boolean = false;
	public selected: Optional<RadioButton> = null;

	constructor(id: string) {
		this.root = document.getElementById(id)!;
		this.buttons = [];

		Array.from(this.root.children).forEach(button => {
			if (button.getAttribute("data-type") != "radio") return;
			let e: HTMLElement = button as HTMLElement;

			e.onclick = () => {
				this.selectButton(e);
			};
			this.buttons.push(new RadioButton(e, this));
		});
	}

	private selectButton(button: HTMLElement) {
		if (this.locked) return;

		this.buttons.forEach(radioButton => {
			if (radioButton.id == button.id) {
				radioButton.select();
			} else {
				radioButton.deselect();
			}
		});
	}

	public getValue(): string {
		if (!this.selected) throw new Error("not selected");
		this.locked = true;

		return this.selected.element.innerHTML.replace(/\s/g, "");
	}
}
